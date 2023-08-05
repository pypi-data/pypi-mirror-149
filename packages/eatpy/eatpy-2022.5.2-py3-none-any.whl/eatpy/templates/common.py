import json
import os

from ..default_files import GITIGNORE, SETTINGS_JSON


################################################################
# Helpers
################################################################
# make dir if not exist and write file
def _makedir_and_write(fp, content, mode="w"):
    # make directory
    _dir = fp.rsplit("/", 1)[0]
    os.makedirs(_dir, exist_ok=True)

    # write file
    _ext = fp.rsplit(".", 1)[-1]
    with open(fp, mode) as f:
        if _ext.lower() in ["json"]:
            json.dump(content, f)
        else:
            f.write(content)


# list of string to setup.cfg format
def _list_to_cfg_format(install_requires: list):
    TAB = "    "
    if install_requires is None:
        return ""

    if "" not in install_requires:
        install_requires = ["", *install_requires]

    return f"\n{TAB}".join(install_requires)


################################################################
# .vscode/setting.json
################################################################
def _generate_vscode_settings(root):
    FILE = ".vscode/settings.json"
    content = SETTINGS_JSON
    fp = os.path.join(root, FILE)
    _makedir_and_write(fp, content)


################################################################
# .gitignore
################################################################
def _generate_gitignore(root):
    FILE = ".gitignore"
    content = GITIGNORE
    fp = os.path.join(root, FILE)
    _makedir_and_write(fp, content)
