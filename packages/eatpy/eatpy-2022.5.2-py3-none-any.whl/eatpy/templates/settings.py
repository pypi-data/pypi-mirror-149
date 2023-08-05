import os

from rich.console import Console
from rich.panel import Panel

from ..default_files import PYPROJECT_TOML, SETUP_CFG
from .common import _generate_gitignore, _generate_vscode_settings, _list_to_cfg_format, _makedir_and_write

console = Console(width=88)

################################################################
# init package
################################################################
def init_settings(root):
    from PyInquirer import prompt

    root = os.path.abspath(root)
    project = root.rsplit("/", 1)[-1]

    q_setup_cfg = [
        {
            "type": "input",
            "name": "install_requires",
            "message": "Python Packages (for requirements.txt)",
            "filter": lambda x: [_.strip() for _ in x.split(",")],
        },
        {
            "type": "input",
            "name": "private_pypi",
            "default": "http://pypi.ml.xscope.ai/simple",
            "message": "Your Private PyPI",
        },
        {
            "type": "checkbox",
            "name": "files",
            "message": "Select Options",
            "choices": [
                {"name": ".gitignore", "checked": True},
                {"name": ".vscode/settings.json", "checked": True},
            ],
        },
        {"type": "confirm", "name": "confirm", "message": "Confirm Initializer"},
    ]
    conf = prompt(q_setup_cfg)
    confirm = conf.pop("confirm")
    if not confirm:
        print("[EXIT] Nothing Happened!")
        return
    files = conf.pop("files")
    if ".vscode/settings.json" in files:
        _generate_vscode_settings(root=root)
    if ".gitignore" in files:
        _generate_gitignore(root=root)
    if len(conf.get("install_requires", [])) > 0:
        _generate_requirements_txt(root, conf=conf)

    summary = "\n".join(
        [
            f"[bold]Python project '{project}' is ready.[/bold]",
        ]
    )

    print()
    console.print(Panel(summary))


################################################################
# requirements.txt
################################################################
def _generate_requirements_txt(root, conf):
    FILE = "requirements.txt"
    install_requires = conf.get("install_requires", "")
    private_pypi = conf.get("private_pypi")
    if private_pypi is not None and private_pypi != "":
        install_requires += [
            f"--extra-index-url {private_pypi}",
            f"--trusted-host {private_pypi.split('://')[-1].rsplit('/', 1)[0]}",
        ]
    content = "\n".join(install_requires)
    fp = os.path.join(root, FILE)
    _makedir_and_write(fp, content)
