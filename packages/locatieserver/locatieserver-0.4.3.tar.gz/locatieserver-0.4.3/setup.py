# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['locatieserver',
 'locatieserver.client',
 'locatieserver.client.tests',
 'locatieserver.schema',
 'locatieserver.schema.tests']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.21.0', 'pydantic>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['locatieserver = locatieserver.__main__:main']}

setup_kwargs = {
    'name': 'locatieserver',
    'version': '0.4.3',
    'description': 'Locatieserver api client',
    'long_description': 'locatieserver\n===========================\n\n|PyPI| |Python Version| |License| |Build| |Tests| |Codecov| |pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/locatieserver.svg\n   :target: https://pypi.org/project/locatieserver/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/locatieserver\n   :target: https://pypi.org/project/locatieserver\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/github/license/foarsitter/locatieserver\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/locatieserver/latest.svg?label=Read%20the%20Docs\n   :target: https://locatieserver.readthedocs.io/\n   :alt: Read the documentation at https://locatieserver.readthedocs.io/\n.. |Build| image:: https://github.com/foarsitter/locatieserver/workflows/Build%20locatieserver%20Package/badge.svg\n   :target: https://github.com/foarsitter/locatieserver/actions?workflow=Package\n   :alt: Build Package Status\n.. |Tests| image:: https://github.com/foarsitter/locatieserver/workflows/Run%20locatieserver%20Tests/badge.svg\n   :target: https://github.com/foarsitter/locatieserver/actions?workflow=Tests\n   :alt: Run Tests Status\n.. |Codecov| image:: https://codecov.io/gh/foarsitter/locatieserver/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/foarsitter/locatieserver\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nThis repository contains a client for the PDOK locatieserver_.\n\n.. _locatieserver: https://foarsitter.github.io/locatieserver/readme.html\n\n\nInstallation\n------------\n\nYou can install *locatieserver* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install locatieserver\n\n\nUsage\n-----\n\nSee for https://foarsitter.github.io/locatieserver/usage.html usage\n\n\n\nCredits\n-------\n\nThis package was created with cookietemple_ using Cookiecutter_ based on Hypermodern_Python_Cookiecutter_.\n\n.. _cookietemple: https://cookietemple.com\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _PyPI: https://pypi.org/\n.. _Hypermodern_Python_Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _pip: https://pip.pypa.io/\n.. _Usage: https://locatieserver.readthedocs.io/en/latest/usage.html\n',
    'author': 'Jelmer Draaijer',
    'author_email': 'info@jelmert.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/foarsitter/locatieserver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
