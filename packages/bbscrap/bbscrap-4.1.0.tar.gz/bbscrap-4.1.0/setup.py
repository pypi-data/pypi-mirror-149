# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbscrap', 'bbscrap.navegacao', 'bbscrap.tratamento', 'bbscrap.utils']

package_data = \
{'': ['*']}

install_requires = \
['ofxparse>=0.21,<0.22', 'pandas>=1.4.1,<2.0.0', 'selenium>=4.1.2,<5.0.0']

entry_points = \
{'console_scripts': ['bbscrap = bbscrap.cli:cli']}

setup_kwargs = {
    'name': 'bbscrap',
    'version': '4.1.0',
    'description': 'Baixa extatos bancários do Banco do Brasil',
    'long_description': None,
    'author': 'Vinicius Maciel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
