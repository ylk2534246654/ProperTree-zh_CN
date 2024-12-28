import downloader
import json, os, sys, argparse

DEFAULT_URL = "https://raw.githubusercontent.com/corpnewt/ProperTree/master/Scripts/version.json"
DEFAULT_TEX_URL = "https://raw.githubusercontent.com/acidanthera/OpenCorePkg/master/Docs/Configuration.tex"
DL = None
try: DL = downloader.Downloader()
except: pass

def _print_output(output):
    print(json.dumps(output,indent=2))

def _get_latest_tex(url = None, file_path = None):
    if DL is None:
        return _print_output({
            "exception":"初始化下载器时发生错误",
            "error":"无法初始化下载器。"
        })
    url = url or DEFAULT_TEX_URL
    if file_path is None:
        return _print_output({
            "exception":"目标文件路径未解析，也未明确提供",
            "error":"缺少必需参数。"
        })
    # We should have a target path and a URL - let's download
    try:
        file_path = DL.stream_to_file(url,file_path,False)
    except:
        return _print_output({
            "exception":"无法从github获取Configuration.tex文件。可能是网络问题。",
            "error":"下载 Configuration.tex 配置文件时出错。"
        })
    # Ensure the path exists
    if not os.path.isfile(file_path):
        return _print_output({
            "exception":"无法从github获取Configuration.tex文件。可能是网络问题。",
            "error":"下载 Configuration.tex 配置文件时出错。"
        })
    _print_output({
        "json":file_path
    })

def _check_for_update(version_url = None):
    if DL is None:
        return _print_output({
            "exception":"无法初始化下载器。",
            "error":"初始化下载器时发生错误"
        })
    version_url = version_url or DEFAULT_URL
    try:
        json_string = DL.get_string(version_url,False)
    except:
        return _print_output({
            "exception":"无法从GitHub获取版本数据。可能是网络问题。",
            "error":"检查更新时发生错误"
        })
    try:
        json_data = json.loads(json_string)
    except:
        return _print_output({
            "exception":"无法将返回的JSON数据进行序列化。",
            "error":"检查更新时发生错误"
        })
    _print_output({
        "json":json_data
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="update_check.py")
    parser.add_argument("-u", "--url", help="覆盖了用于更新/TeX 检查的默认URL")
    parser.add_argument("-m", "--update-mode", help="设置当前的更新模式（更新或TeX） - 默认为更新", choices=["update","tex"])
    parser.add_argument("-t", "--tex-path", help="设置首选的Configuration.tex文件路径（如果使用-m tex选项，则为必需）")

    args = parser.parse_args()

    if not args.update_mode or args.update_mode == "update":
        _check_for_update(version_url=args.url)
    elif args.update_mode == "tex":
        if not args.tex_path:
            _print_output({
                "exception":"在使用-m tex时，需要指定--tex-path",
                "error":"缺少必需的参数"
            })
        else:
            _get_latest_tex(url=args.url,file_path=args.tex_path)
    else:
        _print_output({
            "exception":"未传递有效的--update-mode参数。",
            "error":"无效参数"
        })
