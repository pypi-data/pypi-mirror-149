# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaud']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'environs>=9.4.0,<10.0.0',
 'gitspy>=0,<1',
 'lsfiles>=0,<1',
 'm2r>=0.2.1,<0.3.0',
 'mistune<=0.8.4',
 'object-colors>=2.0.1,<3.0.0',
 'pyaud-plugins>=0,<1',
 'spall>=0,<1',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['pyaud = pyaud.__main__:main']}

setup_kwargs = {
    'name': 'pyaud',
    'version': '3.13.5',
    'description': 'Framework for writing Python package audits',
    'long_description': 'pyaud\n=====\n.. image:: https://github.com/jshwi/pyaud/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/jshwi/pyaud/actions/workflows/ci.yml\n    :alt: ci\n.. image:: https://github.com/jshwi/pyaud/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/jshwi/pyaud/actions/workflows/codeql-analysis.yml\n    :alt: CodeQL\n.. image:: https://readthedocs.org/projects/pyaud/badge/?version=latest\n    :target: https://pyaud.readthedocs.io/en/latest/?badge=latest\n    :alt: readthedocs.org\n.. image:: https://img.shields.io/badge/python-3.8-blue.svg\n    :target: https://www.python.org/downloads/release/python-380\n    :alt: python3.8\n.. image:: https://img.shields.io/pypi/v/pyaud\n    :target: https://img.shields.io/pypi/v/pyaud\n    :alt: pypi\n.. image:: https://codecov.io/gh/jshwi/pyaud/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/jshwi/pyaud\n    :alt: codecov.io\n.. image:: https://img.shields.io/badge/License-MIT-blue.svg\n    :target: https://lbesson.mit-license.org/\n    :alt: mit\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\nThe ``pyaud`` framework is designed for writing modular audits for Python packages\n\n    | Audits can be run to fail, such as when using CI, or include a fix\n    | Fixes can be written for whole directories or individual files\n    | Plugins can be written for manipulating files\n    | Supports single script plugins\n\nInstall\n-------\nDependencies\n\n    | python3.8 (see `pyenv <https://github.com/pyenv/pyenv>`_)\n    | pip\n\nPyPi\n\n``pip install pyaud``\n\nDevelopment\n\n``poetry install``\n\nUsage\n-----\n\n.. code-block:: console\n\n    usage: pyaud [-h] [-c] [-d] [-f] [-s] [-v] [--rcfile RCFILE] MODULE\n\n    positional arguments:\n      MODULE           choice of module: [modules] to list all\n\n    optional arguments:\n      -h, --help       show this help message and exit\n      -c, --clean      clean unversioned files prior to any process\n      -d, --deploy     include test and docs deployment after audit\n      -s, --suppress   continue without stopping for errors\n      -v, --verbose    incrementally increase logging verbosity\n      --rcfile RCFILE  select file to override config hierarchy\n\nPlugins\n-------\n\n``pyaud`` will search for a ``plugins`` package in the project root\n\n    | This package can contain any number of Python modules\n    | For writing plugins see `docs <https://jshwi.github.io/pyaud/pyaud.html#pyaud-plugins>`_\n\nThe following plugins are usable out of the box:\n\n.. code-block:: console\n\n    audit           -- Read from [audit] key in config\n    clean           -- Remove all unversioned package files recursively\n    coverage        -- Run package unit-tests with `pytest` and `coverage`\n    deploy          -- Deploy package documentation and test coverage\n    deploy-cov      -- Upload coverage data to `Codecov`\n    deploy-docs     -- Deploy package documentation to `gh-pages`\n    docs            -- Compile package documentation with `Sphinx`\n    files           -- Audit project data files\n    format          -- Audit code against `Black`\n    format-docs     -- Format docstrings with `docformatter`\n    format-str      -- Format f-strings with `flynt`\n    generate-rcfile -- Print rcfile to stdout\n    imports         -- Audit imports with `isort`\n    lint            -- Lint code with `pylint`\n    readme          -- Parse, test, and assert RST code-blocks\n    requirements    -- Audit requirements.txt with Pipfile.lock\n    tests           -- Run the package unit-tests with `pytest`\n    toc             -- Audit docs/<NAME>.rst toc-file\n    typecheck       -- Typecheck code with `mypy`\n    unused          -- Audit unused code with `vulture`\n    whitelist       -- Check whitelist.py file with `vulture`\n\nEnvironment\n-----------\n\nDefault environment variables:\n\n.. code-block:: shell\n\n    PYAUD_WHITELIST     = "whitelist.py"\n    PYAUD_COVERAGE_XML  = "coverage.xml"\n    PYAUD_REQUIREMENTS  = "requirements.txt"\n    PYAUD_GH_NAME       = ""\n    PYAUD_GH_EMAIL      = ""\n    PYAUD_GH_TOKEN      = ""\n    PYAUD_GH_REMOTE     = ""\n\nEnvironment variables should be placed in an .env file in the project root and override all config files\n\nConfigure\n---------\n\nConfiguration of settings can be made with the following toml syntax files (overriding in this order):\n\n    | ~/.config/pyaud/pyaud.toml\n    | ~/.pyaudrc\n    | .pyaudrc\n    | pyproject.toml\n\nExample config:\n\n.. code-block:: toml\n\n    [clean]\n    exclude = ["*.egg*", ".mypy_cache", ".env", "instance"]\n\n    [logging]\n    version = 1\n    disable_existing_loggers = true\n\n    [indexing]\n    exclude = ["whitelist.py", "conf.py", "setup.py"]\n\n    [packages]\n    exclude = ["tests"]\n    name = "pyaud"\n\n    [audit]\n    modules = [\n        "format",\n        "format-docs",\n        "format-str",\n        "imports",\n        "typecheck",\n        "unused",\n        "lint",\n        "coverage",\n        "readme",\n        "docs",\n    ]\n\n    [logging.root]\n    level = "INFO"\n    handlers = ["default"]\n    propagate = false\n\n    [logging.formatters.standard]\n    format = "%(asctime)s %(levelname)s %(name)s %(message)s"\n\n    [logging.handlers.default]\n    class = "logging.handlers.TimedRotatingFileHandler"\n    formatter = "standard"\n    when = "d"\n    backupCount = 60\n    filename = "~/.cache/pyaud/log/pyaud.log"\n\nPrefix each key with ``tool.pyaud`` when using pyproject.toml\n\n.. code-block:: toml\n\n    [tool.pyaud.clean]\n    exclude = ["*.egg*", ".mypy_cache", ".env", "instance"]\n',
    'author': 'jshwi',
    'author_email': 'stephen@jshwisolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
