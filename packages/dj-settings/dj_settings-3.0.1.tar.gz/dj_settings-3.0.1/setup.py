# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dj_settings']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'tomli>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'dj-settings',
    'version': '3.0.1',
    'description': 'project settings the UNIX way',
    'long_description': '==========================================\ndj_settings: project settings the UNIX way\n==========================================\n\n.. image:: https://github.com/spapanik/dj_settings/actions/workflows/build.yml/badge.svg\n  :alt: Build\n  :target: https://github.com/spapanik/dj_settings/actions/workflows/build.yml\n.. image:: https://img.shields.io/lgtm/alerts/g/spapanik/dj_settings.svg\n  :alt: Total alerts\n  :target: https://lgtm.com/projects/g/spapanik/dj_settings/alerts/\n.. image:: https://img.shields.io/github/license/spapanik/dj_settings\n  :alt: License\n  :target: https://github.com/spapanik/dj_settings/blob/main/LICENSE.txt\n.. image:: https://img.shields.io/pypi/v/dj_settings\n  :alt: PyPI\n  :target: https://pypi.org/project/dj_settings\n.. image:: https://pepy.tech/badge/dj_settings\n  :alt: Downloads\n  :target: https://pepy.tech/project/dj_settings\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :alt: Code style\n  :target: https://github.com/psf/black\n\n``dj_settings`` offers way to add project settings in a way\nthat has been battle-tested for years in numerous UNIX apps,\nreading from the value ``/etc/<conf_path>`` or ``~/.config/<conf_path>``\nor ``<proj_path>/<conf_path>`` or an ``ENV VAR``, allowing overriding\nfrom the next read location.  It\'s mainly targeting django, but it can be\nused as a general settings parser\n\nIn a nutshell\n-------------\n\nInstallation\n^^^^^^^^^^^^\n\nThe easiest way is to use `poetry`_ to manage your dependencies and add *dj_settings* to them.\n\n.. code-block:: toml\n\n    [tool.poetry.dependencies]\n    dj_settings = "^3.0.1"\n\nUsage\n^^^^^\n\n``dj_settings`` will read from various config files to get the value of a variable,\nin a way that\'s very familiar to all UNIX users. It allows setting default values,\nand overriding with ENV VARs.\n\nLinks\n-----\n\n- `Documentation`_\n- `Changelog`_\n\n\n.. _poetry: https://python-poetry.org/\n.. _Changelog: https://github.com/spapanik/dj_settings/blob/main/CHANGELOG.rst\n.. _Documentation: https://dj-settings.readthedocs.io/en/latest/\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/dj_settings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
