# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['steam_totp']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.5"': ['dataclasses==0.7']}

setup_kwargs = {
    'name': 'steam-totp',
    'version': '0.1.2',
    'description': 'Python library to generate Steam-style TOTP auth codes',
    'long_description': '# Steam TOTP\n\nThis library generates Steam-style 5-digit alphanumeric two-factor authentication codes given a shared secret.\n\nWorks on Python >3.6,<4.0, may work on Python 2.7.x but not tested.\n\n## Usage\n\n### Install\nYou can install from PyPi.\n\n```bash\n❯ pip install steam-totp\n```\n\nOr install from GitHub for latest version.\n\n```bash\n❯ pip install https://github.com/shabbywu/python-steam-totp/archive/main.zip\n```\n\n### Examples\n```python\nfrom steam_totp import generate_twofactor_code_for_time\n\ncode = generate_twofactor_code_for_time(shared_secret="your-shared-secret")\n```\n',
    'author': 'shabbywu',
    'author_email': 'shabbywu@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shabbywu/python-steam-totp',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7,<4.0',
}


setup(**setup_kwargs)
