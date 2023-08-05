# eatpy

**Python Template Generator.**



### Installation

----

**Use pipx!**

You can run Python application in isolated environment! (like `brew`, `apt`, `npx`)

```bash
user@host:~$ python -m pip install pipx
user@host:~$ python -m pipx install eatpy
```



### How to use

---

(1) Create a pip installable python package template

```bash
user@host:~$ mkdir my-package
user@host:~$ cd my-package
user@host:~/my-package$ eatpy init package .
? Project Name  my-package
? Author  Woojin Cho
? Author Email  woojin.cho@gmail.com
? Description  Test Template
? Long Description  file: README.md
? Keywords  python, test, template, for, installable, package
? License  MIT License
? Python Requires  >= 3.8
? Install Requires  click, pandas, numpy
? Your Private PyPI  http://my-private.pypi.me/simple
? Select Options  done (3 selections)
? Confirm Initializer  Yes

╭──────────────────────────────────────────────────────────────────────────────────────╮
│ Python project 'my-package' is ready.                                                │
│  - Build Package: 'python -m build', python package 'build' is required.             │
│  - Upload to PyPI: 'twine upload dist/*', python package 'twine is required.         │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```



(2) Create AWS Lambda Image w/ Python application

```bash
user@host:~$ mkdir my-lambda
user@host:~$ cd my-lambda
user@host:~/my-lambda$ eatpy init aws-lambda .
? Lambda Function Name  my-lambda
? Python Version  3.8
? Use Conda Environment?  Yes
? Maintainer  Woojin Cho
? Maintainer Email  woojin.cho@gmail.com
? YUM Requirements  git, wget
? Python Pacakge Requirements  click, numpy, pandas
? Your Private PyPI  http://my-private.pypi.me/simple
? Select Options  done (2 selections)
? Confirm Initializer  Yes

╭──────────────────────────────────────────────────────────────────────────────────────╮
│ Python Lambda Function 'my-lambda' is ready.                                         │
│  - Try './build-and-test.sh'                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```



(3) Create Empty Project w/ formatter and linter (for vscode)

```bash
user@host:~$ mkdir my-settings
user@host:~$ cd my-settings
user@host:~/my-settings$ eatpy init settings .
? Python Packages (for requirements.txt)  numpy, pandas
? Your Private PyPI  http://my-private.pypi.me/simple
? Select Options  done (2 selections)
? Confirm Initializer  Yes

╭──────────────────────────────────────────────────────────────────────────────────────╮
│ Python project 'my-settings' is ready.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────╯
```

