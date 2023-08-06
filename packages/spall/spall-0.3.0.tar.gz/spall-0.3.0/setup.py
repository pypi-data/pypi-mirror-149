# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spall']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spall',
    'version': '0.3.0',
    'description': 'Object-oriented commandline',
    'long_description': 'spall\n=====\n.. image:: https://img.shields.io/badge/License-MIT-yellow.svg\n    :target: https://opensource.org/licenses/MIT\n    :alt: License\n.. image:: https://img.shields.io/pypi/v/spall\n    :target: https://img.shields.io/pypi/v/spall\n    :alt: pypi\n.. image:: https://github.com/jshwi/spall/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/spall/actions/workflows/ci.yml\n    :alt: CI\n.. image:: https://github.com/jshwi/spall/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/spall/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://codecov.io/gh/jshwi/spall/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/spall\n    :alt: codecov.io\n.. image:: https://readthedocs.org/projects/spall/badge/?version=latest\n    :target: https://spall.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nObject-oriented commandline\n---------------------------\n\n\nInstall\n-------\n\n.. code-block:: console\n\n    $ pip install spall\n\nDevelopment\n-----------\n\n.. code-block:: console\n\n    $ pip install spall\n\nUsage\n-----\n\nImport ``Subprocess`` from ``spall``\n\n.. code-block:: python\n\n    >>> from spall import Subprocess\n\nInstantiate individual executables\n\n.. code-block:: python\n\n    >>> cat = Subprocess("cat")\n    >>> echo = Subprocess("echo")\n    >>> fails = Subprocess("false")\n\n\nDefault is to return returncode and print stdout and stderr to console\n\n.. code-block:: python\n\n    >>> returncode = echo.call("Hello, world")\n    Hello, world\n    >>> returncode\n    0\n\nCapture stdout with the ``capture`` keyword argument\n\n.. code-block:: python\n\n    >>> echo.call("Hello, world", capture=True)\n    0\n\nStdout is consumed by calling ``stdout()`` which returns a list\n\n.. code-block:: python\n\n    >>> echo.stdout()\n    [\'Hello, world\']\n    >>> echo.stdout()\n    []\n\nStdout is accrued until ``stdout()`` is called\n\n.. code-block:: python\n\n    >>> echo.call("Hello, world", capture=True)\n    0\n    >>> echo.call("Goodbye, world", capture=True)\n    0\n    >>> echo.stdout()\n    [\'Hello, world\', \'Goodbye, world\']\n    >>> echo.stdout()\n    []\n\nRedirect stdout to /dev/null with the ``devnull`` keyword argument\n\n.. code-block:: python\n\n    >>> echo.call("Hello, world", devnull=True)\n    0\n    >>> echo.stdout()\n    []\n\nPipe stdout to file with the ``file`` keyword argument\n\n.. code-block:: python\n\n    >>> import os\n    >>> import tempfile\n    >>>\n    >>> tmp = tempfile.NamedTemporaryFile(delete=False)\n    >>> echo.call("Hello, world", file=tmp.name)\n    0\n    >>> returncode = cat.call(tmp.name)\n    Hello, world\n    >>> returncode\n    0\n    >>> os.remove(tmp.name)\n\nFailing command will raise a ``subprocess.CalledProcessError``\n\n.. code-block:: python\n\n    >>> import contextlib\n    >>> from subprocess import CalledProcessError\n    >>>\n    >>> with contextlib.redirect_stderr(None):\n    ...     try:\n    ...         returncode = fails.call()\n    ...     except CalledProcessError as err:\n    ...         str(err)\n    "Command \'false\' returned non-zero exit status 1."\n    >>> returncode\n    0\n\nThis, however, will not\n\n.. code-block:: python\n\n    >>> with contextlib.redirect_stderr(None):\n    ...     fails.call(suppress=True)\n    1\n\nAll the keyword arguments above can be set as the default for the instantiated object\n\n.. code-block:: python\n\n    >>> echo = Subprocess("echo", capture=True)\n    >>> echo.call("Hello, world")\n    0\n    >>> echo.stdout()\n    [\'Hello, world\']\n\nWhich can then be overridden\n\n.. code-block:: python\n\n    >>> returncode = echo.call("Hello, world", capture=False)\n    Hello, world\n    >>> returncode\n    0\n    >>> echo.stdout()\n    []\n\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
