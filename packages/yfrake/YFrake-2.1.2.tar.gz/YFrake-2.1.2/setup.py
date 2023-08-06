# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yfrake',
 'yfrake.cache',
 'yfrake.client',
 'yfrake.client.return_types',
 'yfrake.config',
 'yfrake.openapi',
 'yfrake.openapi.modules',
 'yfrake.server']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-cors>=0.7,<0.8',
 'aiohttp-swagger3>=0.7,<0.8',
 'aiohttp>=3.8,<3.9',
 'psutil>=5.9,<5.10',
 'pyyaml>=6.0,<6.1',
 'tomli>=2.0,<2.1']

entry_points = \
{'console_scripts': ['gen-spec = '
                     'yfrake.openapi.generator:generate_openapi_spec']}

setup_kwargs = {
    'name': 'yfrake',
    'version': '2.1.2',
    'description': 'A fast and flexible stock market, forex and cryptocurrencies data provider.',
    'long_description': '# YFrake\n\n<a target="new" href="https://pypi.python.org/pypi/yfrake"><img border=0 src="https://img.shields.io/badge/python-3.10+-blue.svg?label=python" alt="Supported Python versions"></a>\n<a target="new" href="https://github.com/aabmets/yfrake/releases"><img border=0 src="https://img.shields.io/github/v/release/aabmets/yfrake" alt="Latest version released"></a>\n<a target="new" href="https://www.codefactor.io/repository/github/aabmets/yfrake"><img border=0 src="https://img.shields.io/codefactor/grade/github/aabmets/yfrake?label=code quality" alt="CodeFactor code quality"></a>\n<a target="new" href="https://scrutinizer-ci.com/g/aabmets/yfrake/"><img border=0 src="https://img.shields.io/scrutinizer/build/g/aabmets/yfrake" alt="Scrutinizer build inspection"></a>\n<a target="new" href="https://app.codecov.io/gh/aabmets/yfrake"><img border=0 src="https://img.shields.io/codecov/c/github/aabmets/yfrake" alt="Code coverage"></a> \n<br />\n<a target="new" href="https://pypi.python.org/pypi/yfrake"><img border=0 src="https://img.shields.io/pypi/dm/yfrake?label=installs" alt="Installs per month"></a>\n<a target="new" href="https://github.com/aabmets/yfrake/issues"><img border=0 src="https://img.shields.io/github/issues/aabmets/yfrake" alt="Issues on Github"></a>\n<a target="new" href="https://github.com/aabmets/yfrake/blob/main/LICENSE"><img border=0 src="https://img.shields.io/github/license/aabmets/yfrake" alt="License on GitHub"></a>\n<a target="new" href="https://github.com/aabmets/yfrake/stargazers"><img border=0 src="https://img.shields.io/github/stars/aabmets/yfrake?style=social" alt="Stars on GitHub"></a>\n<a target="new" href="https://twitter.com/aabmets"><img border=0 src="https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Ftwitter.com%2Faabmets&label=Say%20Thanks" alt="Say thanks on Twitter"></a>\n\n\n### Description\nYFrake is a fast and flexible stock market, forex and cryptocurrencies data scraper and server [&#91;note1&#93;](#footnote1).\nIt enables developers to ***build powerful apps*** without having to worry about the details of session management or maximizing throughput [&#91;note2&#93;](#footnote2).\n\nYFrake has caching built in to speed up requests even more and to reduce load on the source servers. \nThe cache and other YFrake options are fully customizable through the configuration file.\n\nYFrake can be used as a client to directly return market data to the current program or \nas a ***programmatically controllable server*** to provide market data to other applications.\n\nIn addition, all network requests by the client in ***both*** sync and async modes are ***non-blocking***, \nwhich means that your program can continue executing your code while network requests are in progress.\n\nThe best part about YFrake is its ***built-in swagger API documentation*** which you can use to \nperform test queries and examine the returned responses straight in your web browser.\n\nYFrake is built upon the widely used ***aiohttp*** package and its plugins.\n\n### Documentation\n\nThe tutorials and the reference manual is available at: &nbsp; <a target="new" href="http://yfrake.readthedocs.io">yfrake.readthedocs.io</a>\n\n\n### Contributing\n\nYour suggestions on how to improve the library or the docs are welcome!  \nPlease open an issue with the appropriate label to share your ideas or report bugs.\n\n<br />\n<a id="footnote1"><sup>&#91;note1&#93;:</sup></a> Stock market data is sourced from Yahoo Finance. \n<br/>\n<a id="footnote2"><sup>&#91;note2&#93;:</sup></a> The limits of YFrake are configurable and depend on the capabilities of your system.\n<br/>\n',
    'author': 'Mattias Aabmets',
    'author_email': 'mattias.aabmets@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
