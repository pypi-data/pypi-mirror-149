# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dimfred']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click<8.1.0',
 'easydict>=1.9,<2.0',
 'jsoncomment>=0.4.2,<0.5.0',
 'pluck>=0.2,<0.3',
 'prettyprint>=0.1.5,<0.2.0',
 'psutil>=5.9.0,<6.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'urlpath>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'dimfred',
    'version': '0.16.0',
    'description': 'Tools and abbrevations I use often.',
    'long_description': None,
    'author': 'Dmitrij Vinokour',
    'author_email': 'dimfred.1337@web.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
