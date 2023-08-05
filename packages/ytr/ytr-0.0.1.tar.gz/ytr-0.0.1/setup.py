# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ytr']
install_requires = \
['httpx==0.22.0', 'rich==12.3.0', 'typer==0.4.1']

entry_points = \
{'console_scripts': ['ytr = ytr:main']}

setup_kwargs = {
    'name': 'ytr',
    'version': '0.0.1',
    'description': 'Yandex.Translate prompt',
    'long_description': "# ytr — Yandex.Translate prompt\n\nThis is a CLI for Yandex's translate service. At some point I got tired of opening the website, so I made a CLI.\n\nhttps://user-images.githubusercontent.com/75225148/166159403-a018d890-f1c5-42df-bab3-1d57f991d573.mov\n\n## Installation\n\n```console\npipx install ytr\n```\n\nIf you don't use [`pipx`](https://github.com/pypa/pipx/) yet, install with `pip`:\n\n```console\npip install ytr\n```\n\n## Usage\n\nJust run `ytr`.\n\nBy default it uses `en` and `ru` language hints. You can override this behaviour with `--hints` flag, for example, `ytr --hints en de`.\n\nThat's it: enjoy!\n",
    'author': 'Lev Vereshchagin',
    'author_email': 'mail@vrslev.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vrslev/ytr',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
