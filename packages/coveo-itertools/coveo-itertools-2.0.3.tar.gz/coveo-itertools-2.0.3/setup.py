# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coveo_itertools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coveo-itertools',
    'version': '2.0.3',
    'description': 'Collection-related helpers.',
    'long_description': "# coveo-itertools\n\nAnother spin on iteration goodness.\n\n\n## dict lookup\n\nA one-liner function to retrieve a value from a dictionary:\n\n\n```python\nfrom typing import Dict, Any\nfrom coveo_itertools.lookups import dict_lookup\n\n\nexample: Dict[str, Any] = {'nested': {'key': {'lookup': True}}}\n\nassert dict_lookup(example, 'nested', 'key', 'lookup') == True\nassert dict_lookup(example, 'not', 'there', default=None) is None\n```\n",
    'author': 'Jonathan Piché',
    'author_email': 'tools@coveo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/coveooss/coveo-python-oss/tree/main/coveo-itertools',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
