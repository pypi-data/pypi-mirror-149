# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weather']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'einenlum-weather-project',
    'version': '0.0.2',
    'description': 'A dummy project to get the current temperature',
    'long_description': "# einenlum-weather-project\n\nThis library allows to easily fetch the current temperature (in celsius) for a given city.\n\n## Installation\n\n`poetry add einenlum-weather-project`\n\n## Usage\n\n`import weather`\n\n`weather.get_current_temperature('London') # 19.8`\n",
    'author': 'Yann Rabiller',
    'author_email': 'yann.rabiller@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
