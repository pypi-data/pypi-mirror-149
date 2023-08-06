# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['EorzeaEnv', 'EorzeaEnv.Data']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0']

setup_kwargs = {
    'name': 'eorzeaenv',
    'version': '1.5.2',
    'description': 'Final Fantasy XIV weather & time tools.',
    'long_description': "[![Pypi](https://img.shields.io/pypi/v/eorzeaenv.svg?style=flat-square)](https://pypi.org/project/EorzeaEnv/)\n[![Pypi](https://img.shields.io/pypi/pyversions/eorzeaenv.svg?style=flat-square)](https://pypi.org/project/EorzeaEnv/)\n[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FEltonChou%2FEorzeaEnv%2Fbadge&style=flat-square)](https://github.com/EltonChou/EorzeaEnv/actions)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/EorzeaEnv?style=flat-square)\n\n# EorzeaEnv\n\n+ [CHANGELOG](https://github.com/EltonChou/EorzeaEnv/blob/master/CHANGELOG.md)\n\n## Installation\n```\npip install eorzeaenv\n```\n\n## Usage\n```py\nfrom EorzeaEnv import EorzeaLang\nfrom EorzeaEnv import EorzeaTime\nfrom EorzeaEnv import EorzeaWeather\n```\n\n### Eorzea Time\n\n```sh\n>>> EorzeaTime.now()\n'EorzeaTime(Sixth Embral Moon, 11, 21, 56, Phase:0.50, Althyk)'\n\n>>> EorzeaTime.now().moon\n'Sixth Embral Moon'\n\n>>> EorzeaTime.now().sun\n11\n\n>>> EorzeaTime.now().hour\n21\n\n>>> EorzeaTime.now().minute\n56\n\n>>> EorzeaTime.now().phase\n0.50\n\n>>> EorzeaTime.now().guardian\n'Althyk'\n```\n\n### Weather Forecast\n+ Using period as tuple or list\n```python\n# defalut step value is 5\n# This method return a generator if you need to re-use it save the values as `tuple` or `list`.\nt = tuple(EorzeaTime.weather_period(step=3))\n\n# defalut lang is 'en'\n# defalut strict is True for strict mode\n# False for fuzzy mode: `adsfEureka Pyrosadsf` is valid\nweather_en = EorzeaWeather.forecast('Eureka Pyros', t, strict=True)\nweather_ja = EorzeaWeather.forecast('Eureka Pyros', t, lang=EorzeaLang.JA, strict=True)\nweather_de = EorzeaWeather.forecast('Eureka Pyros', t, lang=EorzeaLang.DE, strict=True)\nweather_fr = EorzeaWeather.forecast('Eureka Pyros', t, lang=EorzeaLang.FR, strict=True)\n```\n```sh\n>>> print(weather_en)\n['Thunder', 'Snow', 'Blizzards']\n\n>>> print(weather_ja)\n['雷', '雪', '吹雪']\n\n>>> print(weather_de)\n['Gewittrig', 'Schnee', 'Schneesturm']\n\n>>> print(weather_fr)\n['Orages', 'Neige', 'Blizzard']\n```\n+ Using period in for-loop\n```py\nweather_en = []\nfor t in EorzeaTime.weather_period(step=3):\n    w = EorzeaWeather.forecast('Eureka Pyros', t)\n    weather_en.append(w)\n```\n```sh\n>>> print(weather_en)\n['Thunder', 'Snow', 'Blizzards']\n```\n+ Using period generator directly\n```py\nweather = EorzeaWeather.forecast('Eureka Pyros', EorzeaTime.weather_period(step=3))\n```\n```sh\n>>> print(weather_en)\n['Thunder', 'Snow', 'Blizzards']\n```\n+ Also support float type\n```py\nweather = EorzeaWeather.forecast('Eureka Pyros', 1603644000.0)\n```\n```sh\n>>> print(weather)\n'Thunder'\n```\n\n\n## Thanks\n- [Rogueadyn-SaintCoinach](https://github.com/Rogueadyn/SaintCoinach)\n",
    'author': 'Elton Chou',
    'author_email': 'plscd748@gmail.com',
    'maintainer': 'Elton Chou',
    'maintainer_email': 'plscd748@gmail.com',
    'url': 'https://github.com/EltonChou/EorzeaEnv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
