import os

from rich.console import Console
from rich.panel import Panel

from ..default_files import PYPROJECT_TOML, SETUP_CFG
from .common import _generate_gitignore, _generate_vscode_settings, _list_to_cfg_format, _makedir_and_write

console = Console(width=88)

################################################################
# init package
################################################################
def init_package(root):
    from PyInquirer import prompt

    root = os.path.abspath(root)
    project = root.rsplit("/", 1)[-1]

    q_setup_cfg = [
        {"type": "input", "name": "project", "default": project, "message": "Project Name"},
        {"type": "input", "name": "author", "message": "Author"},
        {"type": "input", "name": "author_email", "message": "Author Email"},
        {"type": "input", "name": "description", "message": "Description"},
        {"type": "input", "name": "long_description", "default": "file: README.md", "message": "Long Description"},
        {"type": "input", "name": "keywords", "message": "Keywords"},
        {"type": "input", "name": "license", "default": "MIT License", "message": "License"},
        {"type": "input", "name": "python_requires", "default": ">= 3.8", "message": "Python Requires"},
        {
            "type": "input",
            "name": "install_requires",
            "message": "Install Requires",
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
                {"name": "<module>/__init__.py", "checked": True},
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
    _generate_setup_cfg(root=root, **conf)
    _generate_pyproject_toml(root=root)

    if ".vscode/settings.json" in files:
        _generate_vscode_settings(root=root)
    if ".gitignore" in files:
        _generate_gitignore(root=root)
    if "<module>/__init__.py" in files:
        _module_init = os.path.join("src", project.replace("-", "_"), "__init__.py")
        _module_init_abs = os.path.join(root, _module_init)
        if not os.path.exists(_module_init_abs):
            os.makedirs(_module_init_abs.rsplit("/", 1)[0], exist_ok=True)
            with open(_module_init_abs, "w") as f:
                f.write(f"# MODULE NAME: {project}")
                f.write("")

    summary = "\n".join(
        [
            f"[bold]Python project '{project}' is ready.[/bold]",
            " - Build Package: 'python -m build', python package 'build' is required.",
            " - Upload to PyPI: 'twine upload dist/*', python package 'twine is required.",
        ]
    )

    print()
    console.print(Panel(summary))


################################################################
# setup.cfg
################################################################
def _generate_setup_cfg(root, **kwargs):
    FILE = "setup.cfg"
    install_requires = _list_to_cfg_format(install_requires=kwargs.get("install_requires"))
    dependency_links = kwargs.get("private_pypi")
    content = (
        SETUP_CFG.replace("{PROJECT}", kwargs.get("project"))
        .replace("{DESCRIPTION}", kwargs.get("description"))
        .replace("{LONG_DESCRIPTION}", kwargs.get("long_description"))
        .replace("{AUTHOR}", kwargs.get("author"))
        .replace("{AUTHOR_EMAIL}", kwargs.get("author_email"))
        .replace("{KEYWORDS}", kwargs.get("keywords"))
        .replace("{LICENSE}", kwargs.get("license"))
        .replace("{DEPENDENCY_LINKS}", kwargs.get("private_pypi"))
        .replace("dependency_links = {DEPENDENCY_LINKS}\n", "")
        .replace("{PYTHON_REQUIRES}", kwargs.get("python_requires"))
        .replace("{INSTALL_REQUIRES}", install_requires)
    )
    fp = os.path.join(root, FILE)
    _makedir_and_write(fp, content)


################################################################
# pyproject.toml
################################################################
def _generate_pyproject_toml(root):
    FILE = "pyproject.toml"
    content = PYPROJECT_TOML
    fp = os.path.join(root, FILE)
    _makedir_and_write(fp, content)
