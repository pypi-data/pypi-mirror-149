# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_n26', 'beancount_n26.utils']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.2,<3.0']

setup_kwargs = {
    'name': 'beancount-n26',
    'version': '0.6.0',
    'description': 'Beancount Importer for N26 CSV exports',
    'long_description': '# Beancount N26 Importer\n\n[![image](https://github.com/siddhantgoel/beancount-n26/workflows/beancount-n26/badge.svg)](https://github.com/siddhantgoel/beancount-n26/workflows/beancount-n26/badge.svg)\n\n[![image](https://img.shields.io/pypi/v/beancount-n26.svg)](https://pypi.python.org/pypi/beancount-n26)\n\n[![image](https://img.shields.io/pypi/pyversions/beancount-n26.svg)](https://pypi.python.org/pypi/beancount-n26)\n\n[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n`beancount-n26` provides a [Beancount] Importer for converting CSV exports of\n[N26] account summaries to the Beancount format.\n\n## Installation\n\n```sh\n$ pip install beancount-n26\n```\n\nIn case you prefer installing from the Github repository, please note that\n`main` is the development branch so `stable` is what you should be installing\nfrom.\n\n## Usage\n\n```python\nfrom beancount_n26 import N26Importer\n\nCONFIG = [\n    N26Importer(\n        IBAN_NUMBER,\n        \'Assets:N26\',\n        language=\'en\',\n        file_encoding=\'utf-8\',\n    ),\n]\n```\n\n### Classification\n\nTo classify specific recurring transactions automatically, you can specify an `account_patterns` as follows:\n\n```python\nfrom beancount_n26 import N26Importer\n\nCONFIG = [\n    N26Importer(\n        IBAN_NUMBER,\n        \'Assets:N26\',\n        language=\'en\',\n        file_encoding=\'utf-8\',\n        account_patterns={\n           "Expenses:Food:Restaurants": [\n              "amorino",\n              "five guys.*",\n           ]\n        }\n    ),\n]\n```\n\nThe keys should be `accounts` while the items in the list are regular expressions that should match a `payee`.\n\nSome helper functions in `beancount_n26/utils/patterns_generation.py` are here to help you generate this dictionnary.\n\n## Contributing\n\nPlease make sure you have Python 3.6+ and [Poetry] installed.\n\n1. Git clone the repository -\n   `git clone https://github.com/siddhantgoel/beancount-n26`\n\n2. Install the packages required for development -\n   `poetry install`\n\n3. That\'s basically it. You should now be able to run the test suite -\n   `poetry run py.test`.\n\n[Beancount]: http://furius.ca/beancount/\n[N26]: https://n26.com/\n[Poetry]: https://poetry.eustace.io/\n',
    'author': 'Siddhant Goel',
    'author_email': 'me@sgoel.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/siddhantgoel/beancount-n26',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
