# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dsalgo',
 'dsalgo_numba',
 'dsalgo_numba.deque',
 'dsalgo_numba.fifo_queue',
 'dsalgo_numba.lca',
 'dsalgo_numba.lca.eulertour_rmq',
 'dsalgo_numba.lca.eulertour_rmq.segtree',
 'dsalgo_numba.maximum_flow',
 'dsalgo_numba.mst',
 'dsalgo_numba.multiset',
 'dsalgo_numba.segpointgetrange',
 'dsalgo_numba.setrangegetpoint',
 'dsalgo_numba.setrangegetrange',
 'dsalgo_numba.tree',
 'dsalgo_numpy']

package_data = \
{'': ['*']}

install_requires = \
['networkx', 'numba==0.55.1', 'numpy', 'optext-python==0.1.1', 'scipy']

extras_require = \
{'docs': ['furo',
          'myst-parser',
          'pdoc3',
          'pydata-sphinx-theme',
          'python-docs-theme',
          'sphinx',
          'sphinx-book-theme',
          'sphinx-theme-pd',
          'sphinx_rtd_theme<=2.0.0',
          'sphinxcontrib-mermaid']}

setup_kwargs = {
    'name': 'dsalgo',
    'version': '0.2.4',
    'description': 'A package for datastructures and algorithms.',
    'long_description': '# DsAlgo: Datastructures and Algorithms for Python\nDsAlgo is a package for Datastructures and Algorithms written in Python.\n\n[![Python package][ci-badge]][ci-url]\n[![readthedocs build status][docs-badge]][docs-url]\n[![pre-commit][pre-commit-badge]][pre-commit-url]\n[![CodeQL][codeql-badge]][codeql-url]\n[![License: MIT][mit-badge]][mit-url]\n[![PyPI version][pypi-badge]][pypi-url]\n[![Github pages][gh-pages-badge]][gh-pages-url]\n\n[ci-badge]: https://github.com/kagemeka/dsalgo-python/actions/workflows/python-package.yml/badge.svg\n[ci-url]: https://github.com/kagemeka/dsalgo-python/actions/workflows/python-package.yml\n[docs-badge]: https://readthedocs.org/projects/dsalgo/badge/?version=latest\n[docs-url]: https://dsalgo.readthedocs.io\n[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n[pre-commit-url]: https://github.com/pre-commit/pre-commit\n[codeql-badge]: https://github.com/kagemeka/dsalgo-python/actions/workflows/codeql-analysis.yml/badge.svg\n[codeql-url]: https://github.com/kagemeka/dsalgo-python/actions/workflows/codeql-analysis.yml\n[mit-badge]: https://img.shields.io/badge/License-MIT-blue.svg\n[mit-url]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://badge.fury.io/py/dsalgo.svg\n[pypi-url]: https://badge.fury.io/py/dsalgo\n[gh-pages-badge]: https://github.com/kagemeka/dsalgo-python/actions/workflows/pages/pages-build-deployment/badge.svg\n[gh-pages-url]: https://kagemeka.github.io/dsalgo-python\n\n\n## Installation\n\nDsAlgo can be installed using pip:\n\n```bash\n$ python3 -m pip install -U dsalgo\n```\n\nIf you want to run the latest version of the code, you can install from git:\n\n```bash\n$ python3 -m pip install -U git+git://github.com/kagemeka/dsalgo-python.git\n```\n\n## Contributing\n\nsee [CONTRIBUTING.md](./.github/docs/CONTRIBUTING.md)\n',
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://kagemeka.github.io/dsalgo-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
