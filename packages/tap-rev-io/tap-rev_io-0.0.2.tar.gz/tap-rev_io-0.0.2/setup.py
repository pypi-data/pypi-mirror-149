# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_rev_io', 'tap_rev_io.tests']

package_data = \
{'': ['*'], 'tap_rev_io': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.4.7,<0.5.0']

entry_points = \
{'console_scripts': ['tap-rev_io = tap_rev_io.tap:Taprev_io.cli']}

setup_kwargs = {
    'name': 'tap-rev-io',
    'version': '0.0.2',
    'description': '`tap-rev_io` is a Singer tap for rev_io, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'BI4ALL',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
