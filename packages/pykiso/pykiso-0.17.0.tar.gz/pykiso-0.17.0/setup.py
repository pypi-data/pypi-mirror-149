# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pykiso',
 'pykiso.interfaces',
 'pykiso.lib',
 'pykiso.lib.auxiliaries',
 'pykiso.lib.auxiliaries.instrument_control_auxiliary',
 'pykiso.lib.auxiliaries.simulated_auxiliary',
 'pykiso.lib.auxiliaries.udsaux',
 'pykiso.lib.connectors',
 'pykiso.lib.connectors.cc_socket_can',
 'pykiso.lib.robot_framework',
 'pykiso.test_coordinator',
 'pykiso.test_setup']

package_data = \
{'': ['*']}

install_requires = \
['MarkupSafe>=2.0,<2.1',
 'PyVISA',
 'PyVISA-py',
 'PyYAML',
 'click',
 'pykiso-python-uds-alpha>=2.0.2,<3.0.0',
 'pylink-square>=0.12.0,<0.13.0',
 'pyserial',
 'python-can[pcan]>=4.0.0,<5.0.0',
 'robotframework==3.2.2',
 'unittest-xml-reporting']

entry_points = \
{'console_scripts': ['instrument-control = '
                     'pykiso.lib.auxiliaries.instrument_control_auxiliary.instrument_control_cli:main',
                     'pykiso = pykiso.cli:main']}

setup_kwargs = {
    'name': 'pykiso',
    'version': '0.17.0',
    'description': 'Embedded integration testing framework.',
    'long_description': '# PyKiso\n\n![Optional Text](./docs/images/pykiso_logo.png)\n\n## Introduction ##\n\n**pykiso** is an integration test framework. With it, it is possible to write\n* Whitebox integration tests directly on my target device\n* Graybox integration tests to make sure the communication-link with my target device is working as expected\n* Blackbox integration tests to make sure my external device interfaces are working as expected\n\nThe project will contain:\n* The core python framework (this repository)\n* Framework plugins that are generic enough to be integrated as "native" (this repository)\n* Additional "testApps" for different targets platforms (e.g. stm32, ...) or languages (C, C++, ...) . It could be pure SW or also HW (other repositories)\n\n## Requirements ##\n\n* Python 3.7+\n* pip/poetry (used to get the rest of the requirements)\n\n## Install ##\n\n```bash\npip install pykiso\n```\n\n[Poetry](https://python-poetry.org/) is more appropriate for developers as it automatically creates virtual environments.\n\n```bash\ncd kiso-testing\npoetry install\npoetry shell\n```\n\n### Pre-Commit\n\nTo improve code-quality, a configuration of [pre-commit](https://pre-commit.com/) hooks are available.\nThe following pre-commit hooks are used:\n\n- black\n- flake8\n- isort\n- trailing-whitespace\n- end-of-file-fixer\n- check-docstring-first\n- check-json\n- check-added-large-files\n- check-yaml\n- debug-statements\n\nIf you don\'t have pre-commit installed, you can get it using pip:\n\n```bash\npip install pre-commit\n```\n\nStart using the hooks with\n\n```bash\npre-commit install\n```\n\n## Commit message convention\n\nCommits are sorted into multiple categories based on keywords that can occur at any position as part of the commit message.\n[Category] Keywords\n* [BREAKING CHANGES] BREAKING CHANGE\n* [Features] feat:\n* [Fixes] fix:\n* [Docs] docs:\n* [Styles] style:\n* [Refactors] refactor!:\n* [Performances] perf:\n* [Tests] test:\n* [Build] build:\n* [Ci] ci:\nEach commit is considered only once according to the order of the categories listed above. Merge commits are ignored.\n\nThe tool commitizen can help you to create commits which follows these standards.\n```bash\n# if not yet installed:\npip install -U commitizen==2.20.4\n# helps you to create a commit:\ncz commit\n# or use equivalent short variant:\ncz c\n```\n\n## Generate Changelog\n\nAfter you installed the dev dependencies from the pipfile you are able to\nautogenerate the Changelog.\n\n```bash\ninvoke changelog\n```\n\n## Usage ##\n\nOnce installed the application is bound to `pykiso`, it can be called with the following arguments:\n\n```bash\nUsage: pykiso [OPTIONS] [PATTERN]\n\n  Embedded Integration Test Framework - CLI Entry Point.\n\n  PATTERN: overwrite the test filter pattern from the YAML file (optional)\n\nOptions:\n  -c, --test-configuration-file FILE\n                                  path to the test configuration file (in YAML\n                                  format)  [required]\n\n  -l, --log-path PATH             path to log-file or folder. If not set will\n                                  log to STDOUT\n\n  --log-level [DEBUG|INFO|WARNING|ERROR]\n                                  set the verbosity of the logging\n  --version                       Show the version and exit.\n  -h, --help                          Show this message and exit.\n  --variant                       allow the user to execute a subset of tests\n                                  based on variants\n  --branch-level                  allow the user to execute a subset of tests\n                                  based on branch levels\n  --junit                         enables the generation of a junit report\n  --text                          default, test results are only displayed in\n                                  the console\n  --failfast                      stop the test run on the first error or\n                                  failure\n```\n\nSuitable config files are available in the `examples` folder.\n\n### Demo using example config ##\n\n```bash\ninvoke run\n```\n\n### Running the Tests ##\n\n```bash\ninvoke test\n```\n\nor\n\n```bash\npytest\n```\n',
    'author': 'Sebastian Fischer',
    'author_email': 'sebastian.fischer@de.bosch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pykiso/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
