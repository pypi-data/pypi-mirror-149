# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytoil',
 'pytoil.api',
 'pytoil.cli',
 'pytoil.config',
 'pytoil.editor',
 'pytoil.environments',
 'pytoil.git',
 'pytoil.repo',
 'pytoil.starters']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'aiofiles==0.8.0',
 'anyio==3.5.0',
 'asyncclick==8.0.3.2',
 'cookiecutter==1.7.3',
 'httpx[http2]==0.22.0',
 'humanize==4.0.0',
 'pydantic==1.9.0',
 'questionary==1.10.0',
 'rich==12.3.0',
 'rtoml==0.7.1',
 'thefuzz[speedup]==0.19.0',
 'virtualenv==20.14.1']

entry_points = \
{'console_scripts': ['pytoil = pytoil.cli.root:main']}

setup_kwargs = {
    'name': 'pytoil',
    'version': '0.30.1',
    'description': 'CLI to automate the development workflow.',
    'long_description': '![logo](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/logo.png)\n\n[![License](https://img.shields.io/github/license/FollowTheProcess/pytoil)](https://github.com/FollowTheProcess/pytoil)\n[![PyPI](https://img.shields.io/pypi/v/pytoil.svg?logo=python)](https://pypi.python.org/pypi/pytoil)\n[![GitHub](https://img.shields.io/github/v/release/FollowTheProcess/pytoil?logo=github&sort=semver)](https://github.com/FollowTheProcess/pytoil)\n[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/FollowTheProcess/pytoil)\n[![CI](https://github.com/FollowTheProcess/pytoil/workflows/CI/badge.svg)](https://github.com/FollowTheProcess/pytoil/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/FollowTheProcess/pytoil/branch/main/graph/badge.svg?token=OLMR2P3J6N)](https://codecov.io/gh/FollowTheProcess/pytoil)\n[![Downloads](https://static.pepy.tech/personalized-badge/pytoil?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/pytoil)\n\n> ***toil:***\n> *"Long, strenuous or fatiguing labour"*\n\n* **Source Code**: [https://github.com/FollowTheProcess/pytoil](https://github.com/FollowTheProcess/pytoil)\n\n* **Documentation**: [https://FollowTheProcess.github.io/pytoil/](https://FollowTheProcess.github.io/pytoil/)\n\n![help](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/help.svg)\n\n## What is it?\n\n*pytoil is a small, helpful CLI to take the toil out of software development!*\n\n`pytoil` is a handy tool that helps you stay on top of all your projects, remote or local. It\'s primarily aimed at python developers but you could easily use it to manage any project!\n\npytoil is:\n\n* Easy to use ✅\n* Easy to configure ✅\n* Safe (it won\'t edit your repos at all) ✅\n* Snappy (it\'s asynchronous from the ground up and as much as possible is done concurrently, clone all your repos in seconds!) 💨\n* Useful! (I hope 😃)\n\nSay goodbye to janky bash scripts 👋🏻\n\n## Background\n\nLike many developers I suspect, I quickly became bored of typing repeated commands to manage my projects, create virtual environments, install packages, fire off `cURL` snippets to check if I had a certain repo etc.\n\nSo I wrote some shell functions to do some of this for me...\n\nAnd these shell functions grew and grew and grew.\n\nUntil one day I saw that the file I kept these functions in was over 1000 lines of bash (a lot of `printf`\'s so it wasn\'t all logic but still). And 1000 lines of bash is *waaaay* too much!\n\nAnd because I\'d basically hacked it all together, it was **very** fragile. If a part of a function failed, it would just carry on and wreak havoc! I\'d have to do `rm -rf all_my_projects`... I mean careful forensic investigation to fix it.\n\nSo I decided to make a robust CLI with the proper error handling and testability of python, and here it is! 🎉\n\n## Installation\n\nAs pytoil is a CLI program, I\'d recommend installing with [pipx].\n\n```shell\npipx install pytoil\n```\n\n![pipx-install](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/pipx_install.svg)\n\nYou can always fall back to pip\n\n![pip-install](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/pip_install.svg)\n\npytoil will install everything it needs *in python* to work. However, it\'s full feature set can only be accessed if you have the following external dependencies:\n\n* [git]\n* [conda] (if you work with conda environments)\n* A directory-aware editor e.g. [VSCode] etc. (if you want to use pytoil to automatically open your projects for you)\n* [poetry] (if you want to create poetry environments)\n* [flit] (if you want to create flit environments)\n\n## Quickstart\n\n`pytoil` is super easy to get started with.\n\nAfter you install pytoil, the first time you run it you\'ll get something like this.\n\n![setup](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/setup.svg)\n\nIf you say yes, pytoil will walk you through a few questions and fill out your config file with the values you enter. If you\'d rather not do this interactively, just say no and it will instead put a default config file in the right place for you to edit later.\n\nOnce you\'ve configured it properly, you can do things like...\n\n#### See your local and remote projects\n\n![show-local](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/show_local.svg)\n\n#### See which ones you have on GitHub, but not on your computer\n\n![show-diff](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/show_diff.svg)\n\n#### Easily grab a project, regardless of where it is\n\nThis project is available on your local machine...\n\n![checkout-local](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/checkout_local.svg)\n\nThis one is on GitHub...\n\n![checkout-remote](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/checkout_remote.svg)\n\n#### Create a new project and virtual environment in one go\n\n![new-venv](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/new_venv.svg)\n\n(And include custom packages, see the [docs])\n\n#### And even do this from a [cookiecutter] template\n\n![new-cookie](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/new_cookie.svg)\n\nAnd loads more!\n\npytoil\'s CLI is designed such that if you don\'t specify any arguments, it won\'t do anything! just show you the `--help`. This is called being a \'well behaved\' unix command line tool.\n\nThis is true for any subcommand of pytoil so you won\'t accidentally break anything if you don\'t specify arguments 🎉\n\nAnd if you get truly stuck, you can quickly open pytoil\'s documentation with:\n\n![docs](https://github.com/FollowTheProcess/pytoil/raw/main/docs/img/docs.svg)\n\nCheck out the [docs] for more 💥\n\n## Contributing\n\n`pytoil` is an open source project and, as such, welcomes contributions of all kinds 😃\n\nYour best bet is to check out the [contributing guide] in the docs!\n\n[pipx]: https://pipxproject.github.io/pipx/\n[docs]: https://FollowTheProcess.github.io/pytoil/\n[FollowTheProcess/poetry_pypackage]: https://github.com/FollowTheProcess/poetry_pypackage\n[wasabi]: https://github.com/ines/wasabi\n[httpx]: https://www.python-httpx.org\n[async-click]: https://github.com/python-trio/asyncclick\n[contributing guide]: https://followtheprocess.github.io/pytoil/contributing/contributing.html\n[git]: https://git-scm.com\n[conda]: https://docs.conda.io/en/latest/\n[VSCode]: https://code.visualstudio.com\n[config]: config.md\n[cookiecutter]: https://github.com/cookiecutter/cookiecutter\n[poetry]: https://python-poetry.org\n[flit]: https://flit.readthedocs.io\n',
    'author': 'Tom Fleet',
    'author_email': 'tomfleet2018@gmail.com',
    'maintainer': 'Tom Fleet',
    'maintainer_email': 'tomfleet2018@gmail.com',
    'url': 'https://github.com/FollowTheProcess/pytoil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
