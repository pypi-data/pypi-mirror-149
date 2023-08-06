# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['protein_design']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.4.0,<5.0.0',
 'biopython>=1.79,<2.0',
 'black>=22.1.0,<23.0.0',
 'invoke>=1.6.0,<2.0.0',
 'numpy==1.21.0',
 'pandas==1.1.5',
 'plotly>=5.6.0,<6.0.0',
 'py3Dmol>=1.8.0,<2.0.0',
 'scipy==1.6.1',
 'seaborn>=0.11.2,<0.12.0',
 'sklearn>=0.0,<0.1',
 'torch>=1.10.2,<2.0.0',
 'tqdm>=4.62.3,<5.0.0',
 'typer>=0.4.1,<0.5.0',
 'umap-learn>=0.5.2,<0.6.0']

setup_kwargs = {
    'name': 'protein-design',
    'version': '1.0.0',
    'description': 'Python tools for protein design',
    'long_description': None,
    'author': 'Tianyu Lu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
