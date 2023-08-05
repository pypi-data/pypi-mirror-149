# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['citric']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6,<5.0'],
 'docs': ['sphinx==4.5.0',
          'sphinx-autodoc-typehints==1.18.1',
          'sphinx-autoapi==1.8.4',
          'myst-parser==0.17.2',
          'furo==2022.4.7',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-copybutton>=0.5.0,<0.6.0'],
 'jupyter': ['jupyterlab>=3.2.5,<4.0.0', 'ipykernel>=6.8.0,<7.0.0']}

setup_kwargs = {
    'name': 'citric',
    'version': '0.0.13',
    'description': 'A client to the LimeSurvey Remote Control API 2, written in modern Python.',
    'long_description': "# Citric\n\n[![Tests][tests-badge]][tests-link]\n[![License](https://img.shields.io/github/license/edgarrmondragon/citric)](https://github.com/edgarrmondragon/citric/blob/master/LICENSE)\n[![Documentation Status][docs-badge]][docs-link]\n[![codecov][codecov-badge]][codecov-link]\n[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fedgarrmondragon%2Fcitric.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fedgarrmondragon%2Fcitric?ref=badge_shield)\n[![PyPI version][pypi-badge]][pypi-link]\n[![Python versions][versions-badge]][pypi-link]\n[![PyPI - Downloads][downloads-badge]][pypi-link]\n[![PyPI - Format](https://img.shields.io/pypi/format/citric)][pypi-link]\n![GitHub languages](https://img.shields.io/github/languages/top/edgarrmondragon/citric)\n![GitHub repo size](https://img.shields.io/github/repo-size/edgarrmondragon/citric)\n![GitHub stars](https://img.shields.io/github/stars/edgarrmondragon/citric)\n[![Github last-commit](https://img.shields.io/github/last-commit/edgarrmondragon/citric)](https://github.com/edgarrmondragon/citric/commits/master)\n\nA client to the LimeSurvey Remote Control API 2, written in modern\nPython.\n\n## Installation\n\n```console\n$ pip install citric\n```\n\n## Documentation\n\nCode samples and API documentation are available at [citric.readthedocs.io](https://citric.readthedocs.io/).\n\n## Contributing\n\nIf you'd like to contribute to this project, please see the [contributing guide](https://citric.readthedocs.io/en/latest/contributing/getting-started.html).\n\n## Credits\n\n- [Claudio Jolowicz][claudio] and [his amazing blog post][hypermodern].\n\n[claudio]: https://twitter.com/cjolowicz/\n[hypermodern]: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n\n<!--Badges-->\n[docs-badge]: https://readthedocs.org/projects/citric/badge/?version=latest\n[docs-link]: https://citric.readthedocs.io/en/latest/?badge=latest\n[updates-badge]: https://pyup.io/repos/github/edgarrmondragon/citric/shield.svg\n[codecov-badge]: https://codecov.io/gh/edgarrmondragon/citric/branch/master/graph/badge.svg\n[codecov-link]: https://codecov.io/gh/edgarrmondragon/citric\n[tests-badge]: https://github.com/edgarrmondragon/citric/workflows/Tests/badge.svg\n[tests-link]: https://github.com/edgarrmondragon/citric/actions?workflow=Tests\n[pypi-badge]: https://img.shields.io/pypi/v/citric.svg?color=blue\n[versions-badge]: https://img.shields.io/pypi/pyversions/citric.svg\n[downloads-badge]: https://img.shields.io/pypi/dm/citric?color=blue\n[pypi-link]: https://pypi.org/project/citric\n\n\n## License\n[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fedgarrmondragon%2Fcitric.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fedgarrmondragon%2Fcitric?ref=badge_large)\n",
    'author': 'Edgar Ramírez-Mondragón',
    'author_email': 'edgarrm358@gmail.com',
    'maintainer': 'Edgar Ramírez-Mondragón',
    'maintainer_email': 'edgarrm358@gmail.com',
    'url': 'https://github.com/edgarrmondragon/citric',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
