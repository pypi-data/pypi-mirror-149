# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['playwrightcapture']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.1.1,<2.0.0', 'playwright>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'playwrightcapture',
    'version': '0.1.11',
    'description': 'A simple library to capture websites using playwright',
    'long_description': '# Playwright Capture\n\nSimple replacement for [splash](https://github.com/scrapinghub/splash) using [playwright](https://github.com/microsoft/playwright-python).\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lookyloo/PlaywrightCapture',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
