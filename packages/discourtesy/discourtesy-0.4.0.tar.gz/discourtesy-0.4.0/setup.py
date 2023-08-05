# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discourtesy', 'discourtesy.routes', 'discourtesy.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0',
 'httpx>=0.22.0,<0.23.0',
 'loguru>=0.6.0,<0.7.0',
 'starlette>=0.19.1,<0.20.0',
 'uvicorn>=0.17.6,<0.18.0']

setup_kwargs = {
    'name': 'discourtesy',
    'version': '0.4.0',
    'description': 'A minimal framework to handle Discord interactions.',
    'long_description': '# Discourtesy\n\nDiscourtesy is a minimal framework to handle Discord interactions.\n\n## Installation\n\nDiscourtesy requires [Python 3.10][python-3.10] or higher.\n\nThis package is available on PyPI, so use `pip` or another dependency manager to install it.\n\n```sh\npip install discourtesy\n```\n\n## Introduction\n\nA basic application with a simple beep boop command looks like this.\n\n```py\nimport discourtesy\n\napp = discourtesy.Application(application_id=0, public_key="", token="")\n\n\n@discourtesy.command("beep")\nasync def beep_command(application, interaction):\n    return "boop"\n\n\napp.add_plugin(__name__)\n```\n\nFirst, the Discourtesy package is being imported and an application is being instantiated. Here, the application\'s ID, public key and token are set. This information can be found in [Discord\'s developer portal][discord-developer-portal].\n\nFinally, the `beep` command is created. The callback provides the application instance and the interaction data, but neither is being used here. The file is being added as a plugin, which makes sure that the command is being registered properly.\n\nTo start the web server, use an ASGI server implementation. By default, [`uvicorn`][uvicorn] is included as a dependency in this package.\n\n```sh\nuvicorn filename:app\n```\n\n## Contributing\n\nBefore contributing to Discourtesy, make sure to read through the [contribution guidelines][contribution-guidelines].\n\nThis project is licensed under the terms of the [MIT][mit-license] license.\n\n[contribution-guidelines]: <https://github.com/robinmahieu/discourtesy/blob/stardust/CONTRIBUTING.md>\n[discord-developer-portal]: <https://discord.com/developers/applications>\n[mit-license]: <https://github.com/robinmahieu/discourtesy/blob/stardust/LICENSE>\n[python-3.10]: <https://www.python.org/downloads/>\n[uvicorn]: <https://www.uvicorn.org/>\n',
    'author': 'Robin Mahieu',
    'author_email': 'robin.mahieu@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/robinmahieu/discourtesy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
