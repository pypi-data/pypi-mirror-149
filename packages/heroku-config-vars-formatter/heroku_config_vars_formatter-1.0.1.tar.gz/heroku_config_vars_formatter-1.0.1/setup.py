# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['heroku_config_vars_formatter']

package_data = \
{'': ['*']}

install_requires = \
['pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['heroku_config_vars_formatter = '
                     'heroku_config_vars_formatter.main:main']}

setup_kwargs = {
    'name': 'heroku-config-vars-formatter',
    'version': '1.0.1',
    'description': 'A small utility to set Heroku config vars in a shell.',
    'long_description': None,
    'author': 'Martin Winkel',
    'author_email': 'martin@pythomation.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
