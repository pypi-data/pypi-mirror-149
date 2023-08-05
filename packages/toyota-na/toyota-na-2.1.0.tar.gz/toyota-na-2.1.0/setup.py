# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toyota_na',
 'toyota_na.vehicle',
 'toyota_na.vehicle.entity_types',
 'toyota_na.vehicle.vehicle_generations']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.1.0',
 'aiohttp>=3.8.1,<4.0.0',
 'cryptography>=35.0.1',
 'pytz>=2022.1,<2023.0']

setup_kwargs = {
    'name': 'toyota-na',
    'version': '2.1.0',
    'description': 'Python client for Toyota North America service API',
    'long_description': '# toyota-na\nPython client for Toyota North America service API\n\n## Install\n```\npip install toyota-na\n```\n## Usage\n```\npython -m toyota_na.app -h  # Get help\npython -m toyota_na.app authorize <username> <passworde>\npython -m toyota_na.app get_user_vehicle_list  # List vehicle\npython -m toyota_na.app get_vehicle_status <vin>  # Get vehcicle status\n...\n```\n\n## Known Issues\n1. Door/window status not always up-to-date unless you call `send_refresh_status` first and wait for it to complete (there is no notification that it completed successfully).\n\n## Developer Guide\n### Quick Start\n```\nfrom toyota_na.client import ToyotaOneClient\n\nasync def main():\n    cli = ToyotaOneClient()\n    await cli.auth.login(USERNAME, PASSWORD)\n    vehicle_list = await cli.get_user_vehicle_list()\n    vehicle_status = await cli.get_vehicle_status(vehicle_list[0]["vin"])\n    ...\n```\n\n### Abstracted Interface Example\n```\nfrom toyota_na.client import ToyotaOneClient\nfrom toyota_na.vehicle.vehicle import get_vehicles\n\nasync def main():\n    cli = ToyotaOneClient()\n```\n\n### Contributing\nWe use black and isort for opinionated formatting to ensure a consistent look and feel throughout the codebase no matter the contributor.\nPre-commit is used to guarantee the files being checked-in to the repo are formatted correctly.\n\nFor convenience a vscode project settings file is included as well. Editors other than vscode will require some setup if you wish to have formatting take place while working.\n\nGetting started:\n- Install poetry - https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions\n- Clone the repo\n- `poetry install`\n- `poetry shell`\n- `pre-commit install`\n\n### Samples\nSample responses from API calls are stored in `samples` folder. The data is sourced from real users and from the Toyota app\'s "Demo Mode"\n\n## Credits:\nThanks @DurgNomis-drol for making the original Toyota module and bring up the discussing of Toyota North America.\n\nThanks @visualage for finding the way to authenticate headlessly.\n',
    'author': 'Gavin Ni',
    'author_email': 'gisngy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
