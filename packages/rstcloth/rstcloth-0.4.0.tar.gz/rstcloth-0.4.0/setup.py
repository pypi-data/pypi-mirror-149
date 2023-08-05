# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rstcloth']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'Pygments>=2.12.0,<3.0.0', 'sphinx>=2,<5']

extras_require = \
{'docs': ['sphinx-rtd-theme==1.0.0',
          'sphinx-tabs==3.2.0',
          'sphinx-charts==0.1.2',
          'sphinx-math-dollar==1.2.0']}

setup_kwargs = {
    'name': 'rstcloth',
    'version': '0.4.0',
    'description': 'A simple Python API for generating RestructuredText.',
    'long_description': "[![Build Status](https://travis-ci.com/thclark/rstcloth.svg?branch=master)](https://travis-ci.com/thclark/rstcloth)\n[![codecov](https://codecov.io/gh/thclark/rstcloth/branch/master/graph/badge.svg)](https://codecov.io/gh/thclark/rstcloth)\n[![PyPI version](https://badge.fury.io/py/rstcloth.svg)](https://badge.fury.io/py/rstcloth)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![black-girls-code](https://img.shields.io/badge/black%20girls-code-f64279.svg)](https://www.blackgirlscode.com/)\n[![Documentation Status](https://readthedocs.org/projects/rstcloth/badge/?version=latest)](https://rstcloth.readthedocs.io/en/latest/?badge=latest)\n\n\n# RstCloth\n\nreStructuredText is a powerful human-centric markup language that is\nwell defined, flexible, with powerful tools that make writing and\nmaintaining text easy and pleasurable. Humans can edit\nreStructuredText without the aide of complex editing tools, and the\nresulting source is easy to manipulate and process.\n\nAs an alternative and a supplement, RstCloth is a Python API for\nwriting well formed reStructuredText programatically.\n\nFind the [project documentation here](https://rstcloth.readthedocs.io)\n\n\n## Developer notes\n\nRepo is based on [thclark/python-library-template](https://github.com/thclark/python-library-template):\n - black style\n - sphinx docs with some examples and automatic build\n - pre-commit hooks\n - tox tests\n - travis ci + cd\n - code coverage\n\n### Pre-Commit\n\nYou need to install pre-commit to get the hooks working. Do:\n```\npip install pre-commit\npre-commit install\n```\n\nOnce that's done, each time you make a commit, the following checks are made:\n\n- valid github repo and files\n- code style\n- import order\n- PEP8 compliance\n- documentation build\n- branch naming convention\n\nUpon failure, the commit will halt. **Re-running the commit will automatically fix most issues** except:\n\n- The flake8 checks... hopefully over time Black (which fixes most things automatically already) will negate need for it.\n- You'll have to fix documentation yourself prior to a successful commit (there's no auto fix for that!!).\n\nYou can run pre-commit hooks without making a commit, too, like:\n```\npre-commit run black --all-files\n```\nor\n```\n# -v gives verbose output, useful for figuring out why docs won't build\npre-commit run build-docs -v\n```\n\n\n### Contributing\n\n- Please raise an issue on the board (or add your $0.02 to an existing issue) so the maintainers know\nwhat's happening and can advise / steer you.\n\n- Create a fork of rstcloth, undertake your changes on a new branch, (see `.pre-commit-config.yaml` for branch naming conventions). To run tests and make commits,\nyou'll need to do something like:\n```\ngit clone <your_forked_repo_address>    # fetches the repo to your local machine\ncd rstcloth                    # move into the repo directory\npyenv virtualenv 3.6.9 myenv            # Makes a virtual environment for you to install the dev tools into. Use any python >= 3.6\npyend activate myenv                    # Activates the virtual environment so you don't screw up other installations\npip install -r requirements-dev.txt     # Installs the testing and code formatting utilities\npre-commit install                      # Installs the pre-commit code formatting hooks in the git repo\ntox                                     # Runs the tests with coverage. NB you can also just set up pycharm or vscode to run these.\n```\n\n- Adopt a Test Driven Development approach to implementing new features or fixing bugs.\n\n- Ask the `rstcloth` maintainers *where* to make your pull request. We'll create a version branch, according to the\nroadmap, into which you can make your PR. We'll help review the changes and improve the PR.\n\n- Once checks have passed, test coverage of the new code is >=95%, documentation is updated and the Review is passed, we'll merge into the version branch.\n\n- Once all the roadmapped features for that version are done, we'll release.\n\n\n### Release process\n\nThe process for creating a new release is as follows:\n\n1. Check out a branch for the next version, called `vX.Y.Z`\n2. Create a Pull Request into the `master` branch.\n3. Undertake your changes, committing and pushing to branch `vX.Y.Z`\n4. Ensure that documentation is updated to match changes, and increment the changelog. **Pull requests which do not update documentation will be refused.**\n5. Ensure that test coverage is sufficient. **Pull requests that decrease test coverage will be refused.**\n6. Ensure code meets style guidelines (pre-commit scripts and flake8 tests will fail otherwise)\n7. Address Review Comments on the PR\n8. Ensure the version in `setup.py` is correct and matches the branch version.\n9. Merge to master. Successful test, doc build, flake8 and a new version number will automatically create the release on pypi.\n10. Go to code > releases and create a new release on GitHub at the same SHA.\n\n\n## Documents\n\n### Building documents automatically\n\nThe documentation will build automatically in a pre-configured environment when you make a commit.\n\nIn fact, the way pre-commit works, you won't be allowed to make the commit unless the documentation builds,\nthis way we avoid getting broken documentation pushed to the main repository on any commit sha, so we can rely on\nbuilds working.\n\n\n### Building documents manually\n\n**If you did need to build the documentation**\n\nInstall `doxgen`. On a mac, that's `brew install doxygen`; other systems may differ.\n\nInstall sphinx and other requirements for building the docs:\n```\npip install -r docs/requirements.txt\n```\n\nRun the build process:\n```\nsphinx-build -b html docs/source docs/build\n```\n",
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
