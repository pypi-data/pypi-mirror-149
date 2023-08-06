# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dealib',
 'dealib.dea',
 'dealib.dea.core',
 'dealib.dea.utils',
 'dealib.linprog',
 'dealib.linprog.tests',
 'dealib.tests']

package_data = \
{'': ['*'],
 'dealib.linprog.tests': ['reference/*'],
 'dealib.tests': ['data/banks1/*',
                  'data/banks2/*',
                  'data/banks3/*',
                  'data/charnes/*',
                  'data/simple/*',
                  'reference/add/*',
                  'reference/dea/*',
                  'reference/direct/*',
                  'reference/malmq/*',
                  'reference/mea/*',
                  'reference/sdea/*']}

install_requires = \
['numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'dealib',
    'version': '1.0.0',
    'description': 'Library developed in Python for conducting Data Envelopment Analysis (DEA).',
    'long_description': '## Project description\n\n**dealib** is a library developed in Python for conducting Data Envelopment Analysis (DEA).\n\nUser documentation can be found [https://artyomviryutin.github.io/dealib]().\n\nLibrary provides following models and options:\n\nModels:\n\n1) `Envelopment model`\n2) `Multiplier model`\n3) `Slack model`\n4) `Additive model`\n5) `Super-efficiency model`\n6) `Direct model`\n7) `Multi-directional model`\n\nOrientation:\n\n1) `Input`\n2) `Output`\n\nReturns to scale (RTS):\n\n1) `Variable returns to scale (VRS)`\n2) `Constant returns to scale (CRS)`\n3) `Decreasing returns to scale (DRS)`\n4) `Increasing returns to scale (IRS)`\n\n## Source\n\nThe latest version can be found at [https://github.com/ArtyomViryutin/dealib]()\n\n## Installation\n\n### Using pip\n\n    pip install dealib\n\n### Using git\n\n    git clone https://github.com/ArtyomViryutin/dealib.git\n',
    'author': 'Artyom Viryutin',
    'author_email': 'avviryutin@edu.hse.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArtyomViryutin/DEA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
