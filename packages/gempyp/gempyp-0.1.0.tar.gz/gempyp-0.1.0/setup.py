# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gempyp',
 'gempyp.config',
 'gempyp.data_compare',
 'gempyp.data_compare.common',
 'gempyp.data_compare.configurator',
 'gempyp.data_compare.core',
 'gempyp.data_compare.data',
 'gempyp.data_compare.report',
 'gempyp.data_compare.tools',
 'gempyp.engine',
 'gempyp.engine.executors',
 'gempyp.libs',
 'gempyp.libs.enums',
 'gempyp.libs.exceptions',
 'gempyp.reporter',
 'gempyp.rest_test']

package_data = \
{'': ['*'], 'gempyp.data_compare': ['config/*']}

install_requires = \
['lxml>=4.7.1,<5.0.0',
 'pandas>=1.3.5,<2.0.0',
 'pytest>=6.2.4,<7.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['gempyp = gempyp.gempyp:main']}

setup_kwargs = {
    'name': 'gempyp',
    'version': '0.1.0',
    'description': 'An ecosystem of libraries useful for software development',
    'long_description': '# pygem \n\n[![Python](https://img.shields.io/badge/python-3.7-blue)]()\n[![codecov](https://codecov.io/gh/gem-shubhamshukla/pygem/branch/main/graph/badge.svg)](https://codecov.io/gh/gem-shubhamshukla/pygem)\n[![Documentation Status](https://readthedocs.org/projects/pygem/badge/?version=latest)](https://pygem.readthedocs.io/en/latest/?badge=latest)\n\n\n## Installation\n\n```bash\n$ pip install -i https://test.pypi.org/simple/ pygem\n```\n\n## Features\n\n- TODO\n\n## Dependencies\n\n- TODO\n\n## Usage\n\n- TODO\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://pygem.readthedocs.io/en/latest/\n\n## Contributors\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/gem-shubhamshukla/pygem/graphs/contributors).\n\n### Credits\n\nThis package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).\n',
    'author': 'Ayush Agarwal',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Gemini-Solutions/gempyp',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
