# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hydra_plugins',
 'hydra_plugins.test',
 'sail_on_client',
 'sail_on_client.agent',
 'sail_on_client.configs',
 'sail_on_client.configs.algorithms',
 'sail_on_client.configs.base',
 'sail_on_client.configs.harness',
 'sail_on_client.configs.protocol',
 'sail_on_client.configs.protocol.detection',
 'sail_on_client.configs.protocol.eval',
 'sail_on_client.configs.protocol.feedback',
 'sail_on_client.configs.protocol.resume_session',
 'sail_on_client.configs.protocol.save_attributes',
 'sail_on_client.configs.protocol.save_features',
 'sail_on_client.configs.protocol.use_attributes',
 'sail_on_client.configs.protocol.use_features',
 'sail_on_client.errors',
 'sail_on_client.evaluate',
 'sail_on_client.feedback',
 'sail_on_client.harness',
 'sail_on_client.protocol',
 'sail_on_client.utils']

package_data = \
{'': ['*'], 'hydra_plugins.test': ['algorithms/*', 'harness/*']}

install_requires = \
['hydra-colorlog>=1.1.0,<2.0.0',
 'hydra-core>=1.1.1,<2.0.0',
 'importlib-metadata>=1.6.0',
 'matplotlib>=3.2.2,<4.0.0',
 'nltk>=3.6.7,<4.0.0',
 'numpy>=1.18.3',
 'pandas>=1.0.3',
 'requests>=2.23.0',
 'scriptconfig==0.5.6',
 'tenacity>=7.0.0,<8.0.0',
 'tinker-engine>=0.10.1,<0.11.0',
 'torch>=1.6.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'types-dataclasses>=0.6.4,<0.7.0',
 'ubelt==0.9.2']

entry_points = \
{'console_scripts': ['aggregate-features = '
                     'sail_on_client.aggregate_features:main',
                     'sail-on-client = '
                     'sail_on_client.client_launcher:client_launcher'],
 'smqtk_plugins': ['CONDDAProtocol = sail_on_client.protocol.condda_protocol',
                   'LocalHarness = sail_on_client.harness.local_harness',
                   'MockCONDDAAgent = sail_on_client.agent.mock_condda_agents',
                   'MockONDAgent = sail_on_client.agent.mock_ond_agents',
                   'ONDProtocol = sail_on_client.protocol.ond_protocol',
                   'ParHarness = sail_on_client.harness.par_harness',
                   'PreComputedAgent = '
                   'sail_on_client.agent.pre_computed_detector',
                   'PreComputedReactionAgent = '
                   'sail_on_client.agent.pre_computed_reaction_agent']}

setup_kwargs = {
    'name': 'sail-on-client',
    'version': '0.30.0',
    'description': 'Client and Protocols for DARPA sail-on',
    'long_description': '# Sail-On Client and Protocols\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![CI Workflow](https://github.com/darpa-sail-on/sail-on-client/actions/workflows/ci.yml/badge.svg)](https://gitlab.kitware.com/darpa-sail-on/sail-on-client/-/commits/master)\n[![codecov](https://codecov.io/gh/darpa-sail-on/sail-on-client/branch/master/graph/badge.svg?token=300M5S27NE)](https://codecov.io/gh/darpa-sail-on/sail-on-client)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/darpa-sail-on/sail-on-client)\n\nClient and Protocols for DARPA sail-on\n\n### Protocols present in the repository\n1. [OND](https://drive.google.com/file/d/1W2Ex4-eQl1CrAbv67fAN0OJL8kmRtvt2/view?usp=sharing)\n2. [CONDDA](https://drive.google.com/file/d/1sIDLTgXivaguVfSp3g1qfe7sqiUcvFLA/view?usp=sharing)\n\n## Requirements\n\n1. [Python 3.7](https://www.python.org/downloads/release/python-370/)\n2. [Poetry >= 1.1.0](https://github.com/python-poetry/poetry)\n\n## Installation\n\n1. Install Poetry following the instructions available in the [installation page](https://python-poetry.org/docs/#installation)\n\n2. Clone the repositories associated with different components in a working directory\n    ```\n      git clone https://github.com/darpa-sail-on/sail-on-client.git\n    ```\n   This would create sail-on-client directories in your working directory\n\n\n3. Install the different components in a virtual environment\n   ```\n     cd sail-on-client\n     poetry install\n     poetry shell\n   ```\n\n\n## Running Client and Server with Different Algorithms\n\nNote: If you are using the server setup by PAR, update the `url` to `http://3.32.8.161:5000`\nin sail_on_client/protocol/configuration.json and skip step 1 of running the server.\n\n1. [Instructions for running M6 Algorithms](M6-ALGO.md)\n1. [Instructions for running M12 Algorithms](M12-ALGO.md)\n1. [Instructions for running M18 Algorithms](M18-ALGO.md)\n\n\n## Publishing on PYPI\nsail-on-client uses github actions to publish packages on pypi. The action is triggered when a semver tag is pushed to the repository.\n\nWe support the following version format <major>.<minor>.<patch> and <major>.<minor>.<patch>-alpha.<alpha-version> for tags.\nTo publish a package on pypi, the tag must match with the version maintained in pyproject.toml.\nThis is implemented as a mandatory check in the workflow. Poetry provides support for both querying and bumping version via cli.\nPlease refer to [version](https://python-poetry.org/docs/cli/#version) for more details.\n\nThus to publish sail-on-client on pypi use the following commands\n\n1. Bump the version in pyproject.toml using `poetry version <version_rule>`.\n2. Use poetry version --short to determine the version that would be used in the tag.\n3. Generate and push the tag using\n   ```\n     git tag <package-version>\n     git push origin --tags\n   ```\n\n## Acknowledgement of Support and Disclaimer\n\nThis material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Contract No. HR001120C0055. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the DARPA.\n',
    'author': 'Ameya Shringi',
    'author_email': 'ameya.shringi@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
