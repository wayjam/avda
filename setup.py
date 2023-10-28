# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avda', 'avda.helper']

package_data = \
{'': ['*']}

install_requires = \
['cchardet>=2.1.7,<3.0.0',
 'click>=8.1.7,<9.0.0',
 'lxml>=4.9.3,<5.0.0',
 'requests>=2.31.0,<3.0.0']

entry_points = \
{'console_scripts': ['avda = avda.cli:cli']}

setup_kwargs = {
    'name': 'avda',
    'version': '0.1.0',
    'description': '',
    'long_description': '# avda\n\n工具箱\n\n## Install\n\n1. With [pipx](https://pypa.github.io/pipx/)\n```sh\npipx install git+https://github.com/wayjam/avda.git\n```\n\n2. With Poetry\n\n```sh\ngit clone https://github.com/wayjam/avda.git\ncd avda\npoetry install\n```\n',
    'author': 'WayJam So',
    'author_email': 'imsuwj@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

