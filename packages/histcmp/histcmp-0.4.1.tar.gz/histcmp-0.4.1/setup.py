# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['histcmp']

package_data = \
{'': ['*'],
 'histcmp': ['static/*', 'static/css/*', 'static/css/bulma/*', 'templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'click==8.0.4',
 'hist[plot]>=2.6.0,<3.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.0.0,<12.0.0',
 'typer>=0.4.0,<0.5.0',
 'wasabi>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['histcmp = histcmp.cli:app']}

setup_kwargs = {
    'name': 'histcmp',
    'version': '0.4.1',
    'description': '',
    'long_description': None,
    'author': 'Paul Gessinger',
    'author_email': 'hello@paulgessinger.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
