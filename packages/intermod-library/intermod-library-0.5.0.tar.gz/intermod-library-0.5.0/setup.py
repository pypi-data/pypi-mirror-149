# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['intermod_library']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0', 'numpy>=1.16.5,<1.24.0', 'pandas==1.4.1', 'scipy==1.8']

setup_kwargs = {
    'name': 'intermod-library',
    'version': '0.5.0',
    'description': 'Tools for calculating and viewing intermodulation products and harmonics.',
    'long_description': '================\nintermod-library\n================\n\n\n.. image:: https://img.shields.io/pypi/v/intermod_library.svg\n        :target: https://pypi.python.org/pypi/intermod_library\n\n.. image:: https://ci.appveyor.com/api/projects/status/9g3f22ws5v3rb4ja/branch/master?svg=true\n    :target: https://ci.appveyor.com/project/wboxx1/intermod-library/branch/master\n    :alt: Build status on Appveyor\n\n.. image:: https://pyup.io/repos/github/wboxx1/intermod-library/shield.svg\n     :target: https://pyup.io/repos/github/wboxx1/intermod-library/\n     :alt: Updates\n\nTools for calculating and viewing intermodulation products and harmonics.\n\n\n* Free software: GNU General Public License v3\n\n* Documentation: https://wboxx1.github.io/intermod-library\n\nInstallation:\n-------------\n\n.. code-block:: console\n\n    $ pip install intermod-library\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`wboxx1/cookiecutter-pypackage`: https://github.com/wboxx1/cookiecutter-pypackage-poetry\n',
    'author': 'Will Boxx',
    'author_email': 'wboxx1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wboxx1.github.io/intermod-library',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
