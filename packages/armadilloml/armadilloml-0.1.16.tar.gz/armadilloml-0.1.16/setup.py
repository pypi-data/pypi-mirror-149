# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['armadilloml',
 'armadilloml.templates.examples.transformers',
 'armadilloml.templates.project-template']

package_data = \
{'': ['*'], 'armadilloml.templates.project-template': ['.github/workflows/*']}

install_requires = \
['Flask>=2.1.1,<3.0.0',
 'GitPython>=3.1.27,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'click>=8.0.4,<9.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich-click>=1.2.1,<2.0.0',
 'rich>=12.0.1,<13.0.0']

entry_points = \
{'console_scripts': ['armadilloml = armadilloml:cli']}

setup_kwargs = {
    'name': 'armadilloml',
    'version': '0.1.16',
    'description': '',
    'long_description': None,
    'author': 'Max Davish',
    'author_email': 'mdavish@yext.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
