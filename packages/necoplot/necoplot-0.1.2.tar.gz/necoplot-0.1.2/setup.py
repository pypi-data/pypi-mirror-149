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
    'version': '0.1.2',
    'description': 'Simplify codes to plot grahp by matplotlib',
    'long_description': "# necoplot\n\n## Usage examples\n\n```python:\nimport numpy as np\nimport necoplot as neco\n\nxx = np.linspace(-5,5,20)\nyy = xx*xx\n\n\n# Basic\nwith neco.plot() as ax:\n    ax.plot(xx, yy)\n\n\n# Config figiure\nwith neco.plot(figsize=(4,4), dpi=150, facecolor='silver') as ax:\n    ax.plot(xx, yy)\n\n\n# Config ax by plot() \nwith neco.plot(figsize=(6,4), xlim=(-5,0)) as ax:\n    ax.plot(xx, yy) \n\n\n# Config ax by using config_ax()\nax0 = neco.config_ax(xlim=(1,5), title='title', xscale='log')\n\nwith neco.plot(ax0, figsize=(6,4)) as ax:\n    ax.plot(xx, yy)\n\n\n# Config ax directry\nwith neco.plot() as ax:\n    ax.plot(xx, yy, label='x squared')\n    ax.legend()\n    ax.hlines(y=25, xmin=-5, xmax=5)\n\n\n# Save figure\nwith neco.plot() as ax:\n    ax.plot(xx, yy)\n    neco.save('sample.png', show=False)\n\n\n# Config default values\nneco.config_user_parameters(title='New default title!')\n\nwith neco.plot() as ax:\n    ax.plot(xx, yy)\n\n\n# Reset config\nneco.reset()\n\n```",
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
