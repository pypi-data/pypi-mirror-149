# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['de_workflow']

package_data = \
{'': ['*']}

install_requires = \
['datapane>=0.14.0,<0.15.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.7.0,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.3.0,<13.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['de-workflow = de_workflow.main:app']}

setup_kwargs = {
    'name': 'de-workflow',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Nick Anthony',
    'author_email': 'nanthony007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11.0',
}


setup(**setup_kwargs)
