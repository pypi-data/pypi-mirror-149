# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metahyper', 'metahyper_examples', 'metahyper_examples.minimal']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'dill>=0.3.4,<0.4.0',
 'more-itertools>=8.12.0,<9.0.0',
 'numpy>=1.21.1,<2.0.0',
 'types-PyYAML>=6.0.4,<7.0.0']

setup_kwargs = {
    'name': 'metahyper',
    'version': '0.5.3',
    'description': 'Parallelisation and distribution framework for neural pipeline search algorithms.',
    'long_description': '# Metahyper\n\nParallelisation and distribution framework for neural pipeline search algorithms.\n\nFeatures:\n\n- Asynchronous parallelization and distribution\n- Fault tolerance for crashes and job time limits\n- Agnostic to search space, objective functions, ...\n\n![Python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-informational)\n[![License](https://img.shields.io/badge/license-MIT-informational)](LICENSE)\n\n## Installation\n\nUsing pip\n\n```bash\npip install metahyper\n```\n\n## Usage\n\nPlease see our examples in [metahyper_examples](metahyper_examples).\n\n## Contributing\n\nPlease see our guidelines and guides for contributors at [CONTRIBUTING.md](CONTRIBUTING.md).\n',
    'author': 'Danny Stoll',
    'author_email': 'stolld@cs.uni-freiburg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/automl/metahyper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
