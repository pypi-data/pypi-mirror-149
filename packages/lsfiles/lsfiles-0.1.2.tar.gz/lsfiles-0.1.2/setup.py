# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lsfiles']

package_data = \
{'': ['*']}

install_requires = \
['gitspy>=0,<1']

setup_kwargs = {
    'name': 'lsfiles',
    'version': '0.1.2',
    'description': 'Path object VC index',
    'long_description': 'lsfiles\n=======\n.. image:: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/lsfiles/actions/workflows/ci.yml\n    :alt: ci\n.. image:: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/lsfiles/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://readthedocs.org/projects/lsfiles/badge/?version=latest\n    :target: https://lsfiles.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/lsfiles\n    :target: https://img.shields.io/pypi/v/lsfiles\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/lsfiles/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/lsfiles\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nPath object VC index\n--------------------\n\nIndex versioned .py files\n\nInstall\n-------\n\n``pip install lsfiles``\n\nDevelopment\n-----------\n\n``poetry install``\n\nUsage\n-----\n\n\nThe ``LSFiles`` instance is a list-like object instantiated with an empty index\n\n.. code-block:: python\n\n    >>> from lsfiles import LSFiles\n    >>> from pathlib import Path\n    >>>\n    >>> files = LSFiles()\n    >>> files\n    <LSFiles []>\n\n\nThe ``LSFiles`` index calls ``git ls-files`` and only versioned files are indexed\n\n.. code-block:: python\n\n    >>> files.populate()\n    >>> for path in sorted([p.relative_to(Path.cwd()) for p in files]):\n    ...     print(path)\n    docs/conf.py\n    lsfiles/__init__.py\n    lsfiles/_indexing.py\n    lsfiles/_objects.py\n    lsfiles/_version.py\n    tests/__init__.py\n    tests/_environ.py\n    tests/_test.py\n    tests/conftest.py\n    whitelist.py\n\nThe ``LSFiles`` instance is an index of unique file paths\n\nIt\'s implementation of ``extend`` prevents duplicates\n\n.. code-block:: python\n\n    >>> p1 = Path.cwd() / "f1"\n    >>> p2 = Path.cwd() / "f1"\n    >>>\n    >>> files = LSFiles()\n    >>> files.extend([p1, p2])\n    >>> sorted([p.relative_to(Path.cwd()) for p in files.reduce()])\n    [PosixPath(\'f1\')]\n\nReduce minimizes index to directories and individual files relative to the current working dir\n\nThe list value is returned, leaving the instance unaltered\n\n.. code-block:: python\n\n    >>> p1 = Path.cwd() / "f1"\n    >>>\n    >>> d = Path.cwd() / "dir"\n    >>> p2 = d / "f2"\n    >>> p3 = d / "f3"\n    >>>\n    >>> files = LSFiles()\n    >>> files.extend([p1, p2, p3])\n    >>> sorted(p.relative_to(Path.cwd()) for p in files.reduce())\n    [PosixPath(\'dir\'), PosixPath(\'f1\')]\n\nExclusions can be added on instantiation\n\nExclusions are evaluated by their basename, and does not have to be an absolute path\n\n.. code-block:: python\n\n    >>> p1 = Path.cwd() / "docs" / "conf.py"\n    >>> p2 = Path.cwd() / "lsfiles" / "__init__.py"\n    >>>\n    >>> files = LSFiles(p1.name)\n    >>> files.populate()\n    >>>\n    >>> ps = [str(p) for p in files]\n    >>>\n    >>> assert not str(p1) in ps\n    >>> assert str(p2) in ps\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
