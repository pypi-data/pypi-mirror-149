# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viscars',
 'viscars.data',
 'viscars.evaluation.evaluators',
 'viscars.evaluation.metrics',
 'viscars.namespace',
 'viscars.recommenders',
 'viscars.training',
 'viscars.utils']

package_data = \
{'': ['*']}

install_requires = \
['fast-pagerank>=0.0.4,<0.0.5',
 'matplotlib>=3.4.2,<4.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'rdflib>=6.0.2,<7.0.0']

setup_kwargs = {
    'name': 'viscars',
    'version': '0.0.10',
    'description': 'VisCARS: Knowledge Graph-based Context-Aware Recommender System for Visualizations',
    'long_description': '# VisCARS: Graph-Based Context-Aware Visualization Recommendation System\n\n![version](https://img.shields.io/pypi/v/viscars)\n\n## Installation\n\n```\npip install viscars\n```\n\n## Citation\n',
    'author': 'Pieter Moens',
    'author_email': 'pieter.moens@ugent.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/predict-idlab/VisCARS',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
