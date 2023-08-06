# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dictones']

package_data = \
{'': ['*'],
 'dictones': ['.git/*',
              '.git/hooks/*',
              '.git/info/*',
              '.git/logs/*',
              '.git/logs/refs/heads/*',
              '.git/logs/refs/remotes/origin/*',
              '.git/objects/09/*',
              '.git/objects/16/*',
              '.git/objects/1a/*',
              '.git/objects/2d/*',
              '.git/objects/37/*',
              '.git/objects/5f/*',
              '.git/objects/89/*',
              '.git/objects/94/*',
              '.git/objects/96/*',
              '.git/objects/aa/*',
              '.git/objects/bf/*',
              '.git/objects/e1/*',
              '.git/objects/f6/*',
              '.git/refs/heads/*',
              '.git/refs/remotes/origin/*',
              '.idea/*',
              '.idea/inspectionProfiles/*']}

setup_kwargs = {
    'name': 'dictones',
    'version': '0.1.1',
    'description': 'Little bit better than dict',
    'long_description': "\n## Description\n\nLike dict, but a little bit better\n\n# install\n```\n  pip install dictones\n```\n\n#### import\n\n```python\nfrom dictones import DictOnes\n```\n\n#### Usage\n# 1. Added constructor\n```python\n  filled_dict = DictOnes('first_key, second_key', 'to first key', 'to second key')\n  print(filled_dict.first_key)\n  print(filled_dict.second_key)\n```\n\n#### Output\n\n```http\n'to first key'\n'to second_key'\n```\n\n# 2. Constructor without filling\n```python\n  filled_dict = DictOnes('first_key, second_key')\n  print(filled_dict.first_key)\n  print(filled_dict.second_key)\n  print(filled_dict.key)\n```\n\n#### Output\n\n```http\nNone\nNone\n...raise KeyError(attrname)\nKeyError: 'key'\n```\n\n# 3. Deleting\n```python\nfilled_dict = DictOnes('first_key, second_key')\nprint(filled_dict.first_key)\nprint(filled_dict.second_key)\nprint('second_key' in filled_dict)\ndel filled_dict.second_key\nprint('second_key' in filled_dict)\n```\n#### Output\n```http\nNone\nNone\nTrue\nFalse\n```\n\n# Otherwise it is the same dict",
    'author': 'to101',
    'author_email': 'to101kv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.1,<4.0',
}


setup(**setup_kwargs)
