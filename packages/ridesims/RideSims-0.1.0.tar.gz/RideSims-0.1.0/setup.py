# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ridesims', 'ridesims.rides.Everest', 'ridesims.rides.SplashMountain']

package_data = \
{'': ['*']}

install_requires = \
['PyDirectInput>=1.0.4,<2.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['ridesims = ridesims.cli_app:app']}

setup_kwargs = {
    'name': 'ridesims',
    'version': '0.1.0',
    'description': 'For running automated ride sequences for RideSims.',
    'long_description': '# RideSims\n \nA python package for running ride sequence automation scripts for RideSims.\n\n----\n\n## Working with Poetry\n\nThe commands listed below can be used to install, build, and run the package using Poetry.\n\n\nAdd a library to the dependencies:\n\n```\n$ poetry add <package>\n```\n\n\nInstall the package with its dependencies:\n\n```\n$ poetry install\n```\n\n\nCreate a wheel package:\n\n```\n$ poetry build\n```\n\n\nTest the wheel package:\n\n```\n$ pip install --user /ridesims/dist/ridesims-0.1.0-py3-none-any.whl\n```\n\n----\n\n## Meet the Rides\n\n[Everest 🏔](.\\ridesims\\rides\\Everest\\README.md)\n\n[Splash Mountain 🐰](.\\ridesims\\rides\\SplashMountain\\README.md)\n\n...\n\n\n----\n',
    'author': 'copev313',
    'author_email': 'copev313@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
