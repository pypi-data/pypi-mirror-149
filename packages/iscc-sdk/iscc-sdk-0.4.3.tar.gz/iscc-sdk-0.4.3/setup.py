# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iscc_sdk']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0,<10.0',
 'cython>=0.29,<0.30',
 'install-jdk>=0.3,<0.4',
 'iscc-core>=0.2,<0.3',
 'iscc-schema>=0.3,<0.4',
 'jmespath>=1.0,<2.0',
 'numpy>=1.22.3,<2.0.0',
 'platformdirs>=2.5,<3.0',
 'pytaglib>=1.5,<2.0']

extras_require = \
{':sys_platform == "linux"': ['python-magic>=0.4,<0.5'],
 ':sys_platform == "win32" or sys_platform == "darwin"': ['python-magic-bin>=0.4,<0.5']}

setup_kwargs = {
    'name': 'iscc-sdk',
    'version': '0.4.3',
    'description': 'Software developer kit for creating ISCCs (International Standard Content Codes)',
    'long_description': '# ISCC - Software Development Kit\n\n[![Build](https://github.com/iscc/iscc-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/iscc/iscc-sdk/actions/workflows/ci.yml)\n[![Version](https://img.shields.io/pypi/v/iscc-sdk.svg)](https://pypi.python.org/pypi/iscc-sdk/)\n[![Coverage](https://codecov.io/gh/iscc/iscc-sdk/branch/main/graph/badge.svg?token=7BJ7HJU815)](https://codecov.io/gh/iscc/iscc-sdk)\n[![Quality](https://app.codacy.com/project/badge/Grade/aa791abf9d824f6aa65a8f86b9222c90)](https://www.codacy.com/gh/iscc/iscc-sdk/dashboard)\n[![Downloads](https://pepy.tech/badge/iscc-sdk)](https://pepy.tech/project/iscc-sdk)\n\n`iscc-sdk` is a Python development kit for creating and managing [ISCC](https://core.iscc.codes) (*International Standard Content Code*)\n\n## What is an ISCC\n\nThe ISCC is a similarity preserving identifier for digital media assets.\n\nISCCs are generated algorithmically from digital content, just like cryptographic hashes. However, instead of using a single cryptographic hash function to identify data only, the ISCC uses various algorithms to create a composite identifier that exhibits similarity-preserving properties (soft hash).\n\nThe component-based structure of the ISCC identifies content at multiple levels of abstraction. Each component is self-describing, modular, and can be used separately or with others to aid in various content identification tasks. The algorithmic design supports content deduplication, database synchronization, indexing, integrity verification, timestamping, versioning, data provenance, similarity clustering, anomaly detection, usage tracking, allocation of royalties, fact-checking and general digital asset management use-cases.\n\n## What is `iscc-sdk`\n\n`iscc-sdk` is built on top of `iscc-core` and adds high level features for generating and handling ISCC codes for all the different mediatypes:\n\n- mediatype detection\n- metadata extraction and embedding\n- mediatype specific content extraction and pre-processing\n- iscc indexing and search\n\n## Requirements\n\nPython 3.8 to 3.10\n\nOn Linux and MacOS taglib needs to be installed as a prerequisite.\nOn Ubuntu, Mint and other Debian-Based distributions do:\n\n```shell\nsudo apt install libtag1-dev\n```\n\nOn a Mac, use HomeBrew:\n\n```shell\nbrew install taglib\n```\n\n## Installation\n\nUse the Python package manager [pip](https://pip.pypa.io/en/stable/) to install `iscc-sdk`.\n\n```bash\npip install iscc-sdk\n```\n\n## Documentation\n\n<https://sdk.iscc.codes>\n\n## Project Status\n\nThe ISCC has been accepted by ISO as full work item ISO/AWI 24138 - International Standard Content\nCode and is currently being standardized at TC 46/SC 9/WG 18. https://www.iso.org/standard/77899.html\n\n!!! attention\n\n    The `iscc-sdk` library and the accompanying documentation is under development. API changes and\n    other backward incompatible changes are to be expected until the upcoming v1.5 stable release.\n\n## Maintainers\n[@titusz](https://github.com/titusz)\n\n## Contributing\n\nPull requests are welcome. For significant changes, please open an issue first to discuss your plans. Please make sure to update tests as appropriate.\n\nYou may also want join our developer chat on Telegram at <https://t.me/iscc_dev>.\n\n',
    'author': 'Titusz',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sdk.iscc.codes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
