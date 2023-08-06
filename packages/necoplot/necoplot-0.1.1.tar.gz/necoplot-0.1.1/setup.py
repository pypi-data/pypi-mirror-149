# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['necoplot']

package_data = \
{'': ['*']}

install_requires = \
['japanize-matplotlib>=1.1.3,<2.0.0', 'matplotlib>=3.5.1,<4.0.0']

setup_kwargs = {
    'name': 'necoplot',
    'version': '0.1.1',
    'description': 'Make it easier to plot by matplotlib',
    'long_description': '# necoplot\nunder development',
    'author': 'guneco',
    'author_email': 'gu3fav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guneco',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
