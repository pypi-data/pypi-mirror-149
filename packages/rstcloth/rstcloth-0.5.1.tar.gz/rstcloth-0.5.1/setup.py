# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rstcloth']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Pygments>=2.12.0,<3.0.0',
 'sphinx>=2,<5',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'docs': ['sphinx-rtd-theme==1.0.0',
          'sphinx-tabs==3.2.0',
          'sphinx-charts==0.1.2',
          'sphinx-math-dollar==1.2.0']}

setup_kwargs = {
    'name': 'rstcloth',
    'version': '0.5.1',
    'description': 'A simple Python API for generating RestructuredText.',
    'long_description': '![cd](https://github.com/thclark/rstcloth/actions/workflows/cd.yml/badge.svg)\n[![codecov](https://codecov.io/gh/thclark/rstcloth/branch/main/graph/badge.svg)](https://codecov.io/gh/thclark/rstcloth)\n[![PyPI version](https://badge.fury.io/py/rstcloth.svg)](https://badge.fury.io/py/rstcloth)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Documentation Status](https://readthedocs.org/projects/rstcloth/badge/?version=latest)](https://rstcloth.readthedocs.io/en/latest/?badge=latest)\n\n# RstCloth\n\nreStructuredText is a powerful human-centric markup language that is\nwell defined, flexible, with powerful tools that make writing and\nmaintaining text easy and pleasurable. Humans can edit\nreStructuredText without the aide of complex editing tools, and the\nresulting source is easy to manipulate and process.\n\nAs an alternative and a supplement, RstCloth is a Python API for\nwriting well formed reStructuredText programatically.\n\nFind the [project documentation here](https://rstcloth.readthedocs.io)\n\n## Developer notes\n\nRepo is based on [thclark/python-library-template](https://github.com/thclark/python-library-template):\n\n- vscode `.devcontainer`\n- black style\n- sphinx docs with some examples and automatic build\n- pre-commit hooks\n- tox tests\n- github actions ci + cd\n- code coverage\n\n### Using VSCode\n\nCheck out the repo and use the remote `.devcontainer` to start developing, with everything installed out of the box.\n\n### In other IDEs\n\nUse `poetry --extras docs` to install the project and get started. You also You need to install pre-commit to get the hooks working. Do:\n\n```\npip install pre-commit\npre-commit install && pre-commit install -t commit-msg\n```\n\nOnce that\'s done, each time you make a commit, a wide range of checks are made and the project file formats are applied.\n\nUpon failure, the commit will halt. **Re-running the commit will automatically fix most issues** except:\n\n- The flake8 checks... hopefully over time Black (which fixes most things automatically already) will negate need for it.\n- You\'ll have to fix documentation yourself prior to a successful commit (there\'s no auto fix for that!!).\n\nYou can run pre-commit hooks without making a commit, too, like:\n\n```\npre-commit run black --all-files\n```\n\nor\n\n```\n# -v gives verbose output, useful for figuring out why docs won\'t build\npre-commit run build-docs -v\n```\n\n### Contributing\n\n- Please raise an issue on the board (or add your \\$0.02 to an existing issue) so the maintainers know\n  what\'s happening and can advise / steer you.\n\n- Create a fork of rstcloth, undertake your changes on a new branch, (see `.pre-commit-config.yaml` for branch naming conventions).\n\n- To make life easy for us, use our conventional commits pattern (if you\'ve got pre-commit installed correctly, it\'ll guide you on your first commit) to make your commits (if not, we\'ll try to preserve your history, but might have to squashmerge which would lose your contribution history)\n\n- Adopt a Test Driven Development approach to implementing new features or fixing bugs.\n\n- Ask the `rstcloth` maintainers _where_ to make your pull request. We\'ll create a version branch, according to the\n  roadmap, into which you can make your PR. We\'ll help review the changes and improve the PR.\n\n- Once checks have passed, test coverage of the new code is >=95%, documentation is updated and the Review is passed, we\'ll merge into the version branch.\n\n### Release process\n\nReleases are automated using conventional-commits and GitHub Actions.\n\n## Documents\n\n### Building documents automatically\n\nIn the VSCode `.devcontainer`, the RestructuredText extension should build the docs live for you (right click the `.rst` file and hit "Open Preview").\n\nOn each commit, the documentation will build automatically in a pre-configured environment. The way pre-commit works, you won\'t be allowed to make the commit unless the documentation builds,\nthis way we avoid getting broken documentation pushed to the main repository on any commit sha, so we can rely on\nbuilds working.\n\n### Building documents manually\n\n**If you did need to build the documentation**\n\nInstall `doxgen`. On a mac, that\'s `brew install doxygen`; other systems may differ.\n\nInstall sphinx and other requirements for building the docs:\n\n```\npoetry install --extras docs\n```\n\nRun the build process:\n\n```\nsphinx-build -b html docs/source docs/build\n```\n',
    'author': 'Tom Clark',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thclark/rstcloth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
