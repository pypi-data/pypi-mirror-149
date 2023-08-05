SETUP_CFG = """\
[metadata]
name = {PROJECT}
description = {DESCRIPTION}
long_description = {LONG_DESCRIPTION}
author = {AUTHOR}
author_email = {AUTHOR}
keywords = {KEYWORDS}
license = {LICENSE}

[options]
dependency_links = {DEPENDENCY_LINKS}
python_requires = {PYTHON_REQUIRES}
package_dir =
    =src
packages = find:
install_requires = {INSTALL_REQUIRES}
include_package_data = True

[options.packages.find]
where = src

[options.entry_points]
console_scripts =
    # <cli command> = <module>.<submodule>:<function>
"""
