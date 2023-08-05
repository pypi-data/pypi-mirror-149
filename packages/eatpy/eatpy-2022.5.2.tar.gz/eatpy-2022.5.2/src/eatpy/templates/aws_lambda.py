import os

from rich.console import Console
from rich.panel import Panel

from ..default_files import APP_PY, BUILD_AND_TEST_SH, DOCKERFILE, ENVIRONMENT_YML, DOCKERFILE_CONDA, TASK_PY
from .common import _generate_gitignore, _generate_vscode_settings, _makedir_and_write

console = Console(width=88)

APP_DIR = "app"
APP = "app.py"
HANDLER = "handler"

################################################################
# init package
################################################################
def init_lambda(root):
    from PyInquirer import prompt

    root = os.path.abspath(root)
    lambda_func = root.rsplit("/", 1)[-1]

    questions = [
        {"type": "input", "name": "lambda_func", "default": lambda_func, "message": "Lambda Function Name"},
        {"type": "input", "name": "python_version", "default": "3.8", "message": "Python Version"},
        {"type": "confirm", "name": "use_conda", "message": "Use Conda Environment?"},
        {"type": "input", "name": "maintainer", "message": "Maintainer"},
        {"type": "input", "name": "maintainer_email", "message": "Maintainer Email"},
        {
            "type": "input",
            "name": "yum_requirements",
            "message": "YUM Requirements",
            "filter": lambda x: [_.strip() for _ in x.split(",")],
        },
        {
            "type": "input",
            "name": "install_requires",
            "message": "Python Pacakge Requirements",
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
    conf = prompt(questions)
    confirm = conf.pop("confirm")

    # write common files
    if not confirm:
        print("[EXIT] Nothing Happened!")
        return
    files = conf.pop("files")
    if ".vscode/settings.json" in files:
        _generate_vscode_settings(root=root)
    if ".gitignore" in files:
        _generate_gitignore(root=root)

    # write
    if conf.get("use_conda", False):
        _generate_environment_yml(root=root, conf=conf)
    _generate_requirements_txt(root=root, conf=conf)
    _generate_app_py(root=root, conf=conf)
    _generate_task_py(root=root, conf=None)
    _generate_dockerfile(root=root, conf=conf)
    _generate_build_and_test_sh(root=root, conf=None)

    summary = "\n".join(
        [
            f"[bold]Python Lambda Function '{lambda_func}' is ready.[/bold]",
            " - Try './build-and-test.sh'",
        ]
    )

    print()
    console.print(Panel(summary))


################################################################
# environment.yml
################################################################
def _generate_environment_yml(root, conf):
    if conf.get("use_conda"):
        FILE = "environment.yml"
        content = ENVIRONMENT_YML.replace("{PYTHON_VERSION}", conf.get("python_version", "3.8"))
        fp = os.path.join(root, FILE)
        _makedir_and_write(fp, content)


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


################################################################
# <app>.py
################################################################
def _generate_app_py(root, conf):
    FILE = f"{conf.get('app_name', 'app')}.py"
    content = APP_PY.replace("{HANDLER}", HANDLER)
    fp = os.path.join(root, APP_DIR, FILE)
    _makedir_and_write(fp, content)


################################################################
# task.py
################################################################
def _generate_task_py(root, conf):
    FILE = "task.py"
    content = TASK_PY
    fp = os.path.join(root, APP_DIR, "src", FILE)
    _makedir_and_write(fp, content)


################################################################
# Dockerfile
################################################################
def _generate_dockerfile(root, conf):
    CONTENT = DOCKERFILE if not conf.get("use_conda") else DOCKERFILE_CONDA
    FILE = "Dockerfile"
    python_version = conf.get("python_version", "3.8")
    maintainer = conf.get("maintainer", "")
    maintainer_email = conf.get("maintainer_email", "")
    content = (
        CONTENT.replace("{PYTHON_VERSION}", python_version)
        .replace("{MAINTAINER}", maintainer)
        .replace("{MAINTAINER_EMAIL}", maintainer_email)
        .replace("\nMAINTAINER  <>", "")
        .replace("{APP_DIR}", APP_DIR)
        .replace("{APP}", APP.replace(".py", ""))
        .replace("{HANDLER}", HANDLER)
    )
    fp = os.path.join(root, FILE)
    _makedir_and_write(fp, content)


################################################################
# build-and-test.sh
################################################################
# Dockerfile
def _generate_build_and_test_sh(root, conf):
    FILE = "build-and-test.sh"
    content = BUILD_AND_TEST_SH
    fp = os.path.join(root, FILE)
    _makedir_and_write(fp, content)
    os.chmod(fp, 0o775)
