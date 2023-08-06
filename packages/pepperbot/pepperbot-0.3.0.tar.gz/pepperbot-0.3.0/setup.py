# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pepperbot',
 'pepperbot.adapters.keaimao',
 'pepperbot.adapters.keaimao.api',
 'pepperbot.adapters.keaimao.event',
 'pepperbot.adapters.keaimao.message',
 'pepperbot.adapters.onebot',
 'pepperbot.adapters.onebot.api',
 'pepperbot.adapters.onebot.event',
 'pepperbot.adapters.onebot.models',
 'pepperbot.adapters.onebot.models.api',
 'pepperbot.adapters.onebot.models.events',
 'pepperbot.adapters.telegram',
 'pepperbot.adapters.telegram.api',
 'pepperbot.adapters.telegram.event',
 'pepperbot.core',
 'pepperbot.core.bot',
 'pepperbot.core.event',
 'pepperbot.core.message',
 'pepperbot.core.route',
 'pepperbot.extensions',
 'pepperbot.extensions.action',
 'pepperbot.extensions.command',
 'pepperbot.extensions.command.commands',
 'pepperbot.extensions.log',
 'pepperbot.extensions.scheduler',
 'pepperbot.store',
 'pepperbot.utils']

package_data = \
{'': ['*'], 'pepperbot': ['adapters/keaimao/event/records/*']}

install_requires = \
['APScheduler>=3.7.0,<4.0.0',
 'Pyrogram>=2.0.14,<3.0.0',
 'TgCrypto>=1.2.3,<2.0.0',
 'arrow>=1.0.3,<2.0.0',
 'better-exceptions>=0.3.3,<0.4.0',
 'devtools>=0.6.1,<0.7.0',
 'httpx>=0.21.1,<0.22.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'rich>=11.1.0,<12.0.0',
 'sanic>=21.12.1,<22.0.0']

entry_points = \
{'console_scripts': ['pepperbot = cli:main']}

setup_kwargs = {
    'name': 'pepperbot',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'SSmJaE',
    'author_email': 'shaoxydd8888@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
