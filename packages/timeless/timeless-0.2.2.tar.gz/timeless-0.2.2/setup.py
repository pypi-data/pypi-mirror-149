# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timeless']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.4,<2.0.0', 'python-dateutil>=2.8.2,<3.0.0']

extras_require = \
{':python_version < "3.9"': ['backports.zoneinfo>=0.2.1,<0.3.0'],
 ':sys_platform == "win32"': ['tzdata>=2022.1,<2023.0']}

setup_kwargs = {
    'name': 'timeless',
    'version': '0.2.2',
    'description': 'Datetime for people in a hurry.',
    'long_description': '# Timeless - a datetime toolkit for people in a hurry.\n\n**Timeless** sits on sholders of giants to provide a simple and easy to use datetime\ntoolkit. Simple date ranges, datetime operations and just one import.\n\nThis package is a work in progress and it was created as a study object.\n\n## 🧠 Features\n\n- ✔️ very simple API\n- ✔️ minimal code to get things done\n- ✔️ easy use with other packages\n- ✔️ just one import\n- ✔️ few dependencies\n\n## 📦 Installation\n\n```bash\npip install timeless\n```\n\n## 📝 Why Timeless?\n\nIt provides a simple API, heavily inspired by [Pendulum](https://github.com/sdispater/pendulum).\n\nI love Pendulum, although since last year (maybe 2 years) it doesn\'t seem to be actively maintained. If you like Pendulum, you will like Timeless. If you want a easy to adopt, integrate and expand package, you will like Timeless.\n\n## 💻 Sample usage\n\nTimeless use two main concepts: `Datetime` and `Period`. A datetime is a point in Time, and a Period is a duration.\n\nTimeless doesn`t differentiate between datetime and date objects.\n\nAll datetimes are assumed to be in the UTC+00:00 timezone if any other timezone isn`t specified.\n\n```python\nimport timeless\n\nstart = timeless.datetime(1900, 1, 1, zone="UTC")\nend = start.add(years=1)\n\nend.subtract(months=1)\n\nstart.set(year=2099, month=2, day=26, hour=5, zone="America/Sao_Paulo")\n\nstart.is_past()  # True\nstart.is_future()  # False\nstart.set(year=2099).is_future()  # True\n```\n\n## 📜 Docs\n\nThe docs are under development, but it\'s (very) early stage is already [available](https://ericmiguel.github.io/timeless/).\n\n## 🏗️ Development\n\nTimeless relies on [Poetry](https://github.com/python-poetry/poetry).\n\nInstall the Python dependencies with:\n\n```bash\npoetry install\n```\n\n## ⚗️ Testing\n\n```bash\npoetry run pytest --cov=timeless tests/\n```\n',
    'author': 'ericmiguel',
    'author_email': 'ericmiguel@id.uff.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ericmiguel/timeless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
