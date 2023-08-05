# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['treeish']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.19,<0.20', 'rich>=12.2,<13.0']

setup_kwargs = {
    'name': 'treeish',
    'version': '0.0.2',
    'description': 'Tree function helpers: set ids, get node from ids, fetch nodes with key',
    'long_description': '# Treeish\n\nSome functions to help with tree like (json-ish) python structures.\n\n## Example Data\n\n```python\n>>> data = [\n        {\n            "item": "Preliminary Title",\n            "units": [\n                {\n                    "item": "Chapter 1",\n                    "caption": "Effect and Application of Laws",\n                    "units": [\n                        {\n                            "item": "Article 1",\n                            "content": \'This Act shall be known as the "Civil Code of the Philippines." (n)\\n\',\n                        },\n                        {\n                            "item": "Article 2",\n                            "content": "Laws shall take effect after fifteen days following the completion of their publication either in the Official Gazette or in a newspaper of general circulation in the Philippines, unless it is otherwise provided. (1a)\\n",\n                        },\n                    ],\n                }\n            ],\n        }\n    ]\n```\n\n## Setter of IDs\n\n```python\n>>> from treeish import set_node_ids\n>>> set_node_ids(data)\n# all nodes in the tree will now have an `id` key, e.g.:\n{\n    "item": "Article 1",\n    "content": \'This Act shall be known as the "Civil Code of the Philippines." (n)\\n\',\n    "id": "1.1.1.1"\n},\n```\n\n## Getter of Node by ID\n\n```python\n>>> from treeish import get_node_id\n>>> get_node_id("1.1.1.1")\n{\n    "item": "Article 1",\n    "content": \'This Act shall be known as the "Civil Code of the Philippines." (n)\\n\',\n}\n```\n\n## Fetcher of Values\n\n```python\n>>> from treeish import test_fetch_values_from_key\n>>> list(test_fetch_values_from_key(data[0]), "item")\n[\n    "Preliminary Title",\n    "Chapter 1",\n    "Article 2",\n    "Article 1",\n]\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
