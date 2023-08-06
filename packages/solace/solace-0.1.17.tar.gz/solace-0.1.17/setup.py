# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solace', 'solace.cli']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.4,<2.0.0',
 'Jinja2>=3.1.1,<4.0.0',
 'boltons>=21.0.0,<22.0.0',
 'libmagic>=1.0,<2.0',
 'loguru>=0.6.0,<0.7.0',
 'pyaml>=21.10.1,<22.0.0',
 'python-magic>=0.4.25,<0.5.0',
 'python-multipart>=0.0.5,<0.0.6',
 'starlette>=0.19.0,<0.20.0',
 'typer[all]>=0.4.1,<0.5.0',
 'uvicorn>=0.17.6,<0.18.0',
 'watchgod>=0.8.2,<0.9.0']

entry_points = \
{'console_scripts': ['solace = solace.cli:cli']}

setup_kwargs = {
    'name': 'solace',
    'version': '0.1.17',
    'description': 'A Modern Framework for Building Python Web Apps',
    'long_description': '<h1>\n    <img src="assets/logo.png" style="max-width: 100px; vertical-align:middle; padding-bottom: 15px;">\n    <br />\n Solace Python Framework\n</h1>\n\n\nSolace is a next generation web framework for Python3, inspired by Koa, built on Starlette.\n\n## Goals\n\n- make a framework that enables truly re-usable code\n    - we have a concept of "flows" (lightweight middleware)\n- make a framework that is easily extendable via plugins\n    - Starlette provides a solid core, everything extra is handled via plugins\n\n- provide a "common sense" approach to building web apps\n- enable rapid development and deployment using best practices\n- solve the problem first, then write the code\n\n### Solace is made from Awesome Open Source Projects\n\n- Starlette\n- Typer\n- Poetry\n- Loguru\n- python-dotenv\n- Jinja2\n- Arrow\n- Cerberus\n',
    'author': 'Dan Sikes',
    'author_email': 'dansikes7@gmail.com',
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
