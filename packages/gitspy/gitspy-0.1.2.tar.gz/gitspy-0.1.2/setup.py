# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitspy']

package_data = \
{'': ['*']}

install_requires = \
['spall>=0,<1']

setup_kwargs = {
    'name': 'gitspy',
    'version': '0.1.2',
    'description': 'Intuitive Git for Python',
    'long_description': 'gitspy\n======\n.. image:: https://github.com/jshwi/gitspy/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/gitspy/actions/workflows/ci.yml\n    :alt: ci\n.. image:: https://github.com/jshwi/gitspy/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/gitspy/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://readthedocs.org/projects/gitspy/badge/?version=latest\n    :target: https://gitspy.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/gitspy\n    :target: https://img.shields.io/pypi/v/gitspy\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/gitspy/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/gitspy\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nIntuitive Git for Python\n\n\nInstall\n-------\nDependencies: git ^2.0.0 (tested)\n\n``pip install gitspy``\n\nDevelopment\n\n``poetry install``\n\nExample Usage\n-------------\n\nGet branch\n**********\n\nCapture will store stdout, which can then be consumed by calling `git.stdout()`\n\nDefault is to return returncode and print stdout and stderr to console\n\n.. code-block:: python\n\n    >>> import gitspy\n    >>> git = gitspy.Git()\n    >>> git.init(capture=True)  # [\'...\']\n    0\n\nConsume stdout (a list containing a str)\n\n.. code-block:: python\n\n    >>> len(git.stdout())  # []\n    1\n\nNo commands have been called yet since last call to `stdout` so stdout is empty\n\n.. code-block:: python\n\n    >>> len(git.stdout())  # []\n    0\n\nStdout can be accrued\n\n.. code-block:: python\n\n    >>> git.init(capture=True)  # [\'...\']\n    0\n    >>> git.init(capture=True)  # [\'...\', \'...\']\n    0\n    >>> len(git.stdout())  # []\n    2\n\nStdout is consumed\n\n.. code-block:: python\n\n    >>> len(git.stdout())  # []\n    0\n\nGet commit hash\n***************\n\n.. code-block:: python\n\n    >>> git.rev_parse("HEAD", capture=True)  # [\'...\']\n    0\n    >>> len(git.stdout()[0])  # []\n    40\n',
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
