# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['servicefoundry',
 'servicefoundry.build',
 'servicefoundry.build.clients',
 'servicefoundry.build.deploy',
 'servicefoundry.build.lib',
 'servicefoundry.build.model',
 'servicefoundry.build.package',
 'servicefoundry.build.parser',
 'servicefoundry.cli',
 'servicefoundry.cli.commands',
 'servicefoundry.notebook']

package_data = \
{'': ['*'], 'servicefoundry.build': ['schema/*']}

install_requires = \
['Mako>=1.1.6,<2.0.0',
 'PyJWT>=2.3.0,<3.0.0',
 'PyYAML>=6.0,<7.0',
 'click>=8.0.4,<9.0.0',
 'fastapi>=0.75.0,<0.76.0',
 'importlib-metadata>=4.2,<5.0',
 'importlib-resources>=5.2.0,<6.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'mistune>=0.8.4,<0.9.0',
 'prometheus_client>=0.13.1,<0.14.0',
 'python-socketio[client]>=5.5.2,<6.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich-click>=1.2.1,<2.0.0',
 'rich>=12.0.0,<13.0.0']

entry_points = \
{'console_scripts': ['servicefoundry = servicefoundry.__main__:main',
                     'sfy = servicefoundry.__main__:main']}

setup_kwargs = {
    'name': 'servicefoundry',
    'version': '0.1.20',
    'description': 'Generate deployed services from code',
    'long_description': '# Dev Setup\n\n**Setup a virtual env (or use an existing one)**\n\n```shell\ncd ~/   # or someplace else\npython3.9 -m venv venv39\n```\n\n> prefer using `python3.9-intel` on Apple Silicon\n\n**Activate the virtual environment**\n\n```shell\nsource ~/venv39/bin/activate\n```\n\n**Install `poetry` and `pre-commit`**\n\n```shell\npip install poetry pre-commit\n```\n\n**Git clone**\n\n```shell\ngit clone https://github.com/truefoundry/servicefoundry-cli\n```\n\n**Install pre-commit hooks**\n\n```shell\ncd servicefoundry-cli/\npre-commit install --install-hooks\n```\n\n> You can run the hook manually with `pre-commit run --all-files`\n\n\n\nIt is recommended to go through [Poetry Docs](https://python-poetry.org/docs/) to get a hang of development, testing and\npackaging process\n\n# Local Installation\n\n```shell\npoetry install\n```\n\n# Testing\n\n```shell\npoetry run pytest\n```\n\n# Build distributions\n\n```shell\npoetry build\n```\n\n# Usage :\n\n- Login : `servicefoundry login`\n\n- Init : `servicefoundry init`\n\n- Run : `servicefoundry run`\n\n# Process flow to use the commands\n\n- servicefoundry (should hint to servicefoundry login)\n- servicefoundry login (should hint to init, run from example folder)\n- servicefoundry init (should hint to run)\n- servicefoundry run (should hint to grafanaendpoint and servicefoundry get service <service_id>)\n\n- servicefoundry list workspace\n- servicefoundry list\n',
    'author': 'Abhishek Choudhary',
    'author_email': 'abhichoudhary06@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/innoavator/servicefoundry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
