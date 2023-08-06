# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wifipass']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0', 'fpdf>=1.7.2,<2.0.0', 'qrcode>=7.3.1,<8.0.0']

entry_points = \
{'console_scripts': ['wifiPass = wifiPass:main']}

setup_kwargs = {
    'name': 'wifipass',
    'version': '0.0.2',
    'description': 'Creates a PDF with a QR code of your wifi password.',
    'long_description': '# wifipass\nA tool to create QR codes to share your wifi credentials.\n\n# Prerequisites\nYou need to have `python3` and `pip` installed.\n\n# Installing\n```\npip install wifiPass-propellerpain\n```\n\n# Running\n```\nusage: python -m wifiPass [-h] --ssid SSID --pw PW --format {PNG,PDF,BOTH}\n                   [--out OUT]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --ssid SSID           network name\n  --pw PW               network password\n  --format {PNG,PDF,BOTH}\n  --out OUT             basename for the outputfile(s)\n  ```\n  For example to generate a pdf version:\n  ```\n  python -m wifiPass --ssid YOUR_SSID_HERE --pw YOUR_PW_HERE --format PDF\n  ```\n',
    'author': 'Pierre',
    'author_email': 'pierre.git@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
