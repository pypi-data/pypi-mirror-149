# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paper_neural']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0', 'numpy>=1.22.3,<2.0.0', 'torch>=1.8.2+cu111,<2.0.0']

setup_kwargs = {
    'name': 'paper-neural',
    'version': '0.2.0',
    'description': 'Reunir mecanimos de detecção de fibras de segurança e comparação de features',
    'long_description': None,
    'author': 'wagner',
    'author_email': 'rengaw.luiz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
