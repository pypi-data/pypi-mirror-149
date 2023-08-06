# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['donordrivepython', 'donordrivepython.api', 'donordrivepython.api.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.27.1', 'rich>=12.4.0,<13.0.0', 'xdgenvpy>=2.3.5,<3.0.0']

setup_kwargs = {
    'name': 'donordrivepython',
    'version': '1.4.0',
    'description': 'A utility to access the DonorDrive API',
    'long_description': 'DonorDrivePython\n----------------\n\nA Python reference implementation of the [Donor Drive API](https://github.com/DonorDrive/PublicAPI)\n\nThis project aims to provide a Python package the user could import to create a project to access the Donor Drive API.\n\nFor an example of what you can build to provide extra functionality around the Donor Drive API, see my project, [ElDonationTracker](http://djotaku.github.io/ELDonationTracker/) for the Extra Life charity event. It takes the Donor Drive API information and converts it to text files and HTML files that the gamers can use for live streaming during the Extra Life Event. Currently, it has the API integrated into it. The API implementation there will become the initial release in this repo.\n',
    'author': 'Eric Mesa',
    'author_email': 'ericsbinaryworld@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/djotaku/DonorDrivePython',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
