# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecomment']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['ecomment = ecomment.cli:main']}

setup_kwargs = {
    'name': 'ecomment',
    'version': '0.1.0',
    'description': 'Comments want to be free.',
    'long_description': '# Comment Files\n\nSee the [comments-file-format.md][1] document and the\n[in-code-ecomments.md][2].\n\n[1]: comments-file-format.md\n[2]: in-code-ecomments.md\n',
    'author': 'Jeremiah England',
    'author_email': 'englandtuning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ecomment/ecomment',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
