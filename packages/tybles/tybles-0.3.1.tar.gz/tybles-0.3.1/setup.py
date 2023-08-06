# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tybles', 'tybles.sts']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.2.4,<2.0.0']

extras_require = \
{'beartype': ['beartype>=0.10.4,<0.11.0'],
 'docs': ['ipykernel>=6.13.0,<7.0.0',
          'myst-nb>=0.13.2,<0.14.0',
          'pygments-csv-lexer>=0.1.3,<0.2.0',
          'sphinx==4.3.2',
          'sphinx-autodoc-typehints>=1.17.0,<2.0.0',
          'sphinx-book-theme>=0.2.0,<0.3.0'],
 'typeguard': ['typeguard>=2.13.3,<3.0.0']}

setup_kwargs = {
    'name': 'tybles',
    'version': '0.3.1',
    'description': 'Tybles: simple schemas for Pandas dataframes',
    'long_description': '# Tybles: simple schemas for Pandas dataframes\n\nSee the website https://denisrosset.github.io/tybles \n\n\n## How to compile the documentation\n\n```bash\npoetry install -E docs -E beartype -E typeguard # important, install the documentation extras\npoetry run make -C docs clean html\n```\n',
    'author': 'Denis Rosset',
    'author_email': 'physics@denisrosset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/denisrosset/tybles.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
