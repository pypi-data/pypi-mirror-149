# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrape_glosbe_dict']

package_data = \
{'': ['*']}

install_requires = \
['cchardet>=2.1.7,<3.0.0',
 'httpx>=0.22.0,<0.23.0',
 'icecream>=2.1.1,<3.0.0',
 'install>=1.3.5,<2.0.0',
 'joblib>=1.1.0,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pyquery>=1.4.3,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'set-loglevel>=0.1.1,<0.2.0',
 'tenacity>=8.0.1,<9.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.64.0,<5.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['scrape-glosbe-dict = scrape_glosbe_dict.__main__:app']}

setup_kwargs = {
    'name': 'scrape-glosbe-dict',
    'version': '0.1.1',
    'description': 'Scrape glosbe dicts given a head words file',
    'long_description': "# scrape-glosbe-dict\n[![pytest](https://github.com/ffreemt/scrape-glosbe-dict/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/scrape-glosbe-dict/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/scrape_glosbe_dict.svg)](https://badge.fury.io/py/scrape_glosbe_dict)\n\nScrape a glosbe dict\n\n## Install it\n\n```shell\npip install scrape-glosbe-dict\n\n# pip install git+https://github.com/ffreemt/scrape-glosbe-dict\n# poetry add git+https://github.com/ffreemt/scrape-glosbe-dict\n# git clone https://github.com/ffreemt/scrape-glosbe-dict && cd scrape-glosbe-dict\n```\n\n## Use it\n```bash\nscrape-glosbe-dict head-word-file  # default english-chinese\n\n# or python -m scrape_glosbe_dict head-word-file\n\n# scrape-glosbe-dict head-word-file -f de  # german-chinese\n```\n\nhead word file formt: one word/phrase per line, empty lines will be ignored.\n\noutput will be saved to a tsv file.\n\n## Docs\n```bash\npython -m scrape_glosbe_dict --help\n```\n```bash\nUsage: python -m scrape_glosbe_dict [OPTIONS] head-word-file\n\nArguments:\n  head-word-file  Head word file, one word/phrase per line, each will be used\n                  to fetch corresponding definitons from https://glosbe.com/.\n                  [required]\n\nOptions:\n  -f, --from-lang TEXT  Source language, check https://glosbe.com/ for valid\n                        value, e.g. https://glosbe.com/en/zh implies\n                        from_lang='en'.  [default: en]\n  -t, --to-lang TEXT    Target language, check https://glosbe.com/ for valid\n                        value, e.g. https://glosbe.com/en/zh implies\n                        to_lang='zh'.  [default: zh]\n  -v, --verbose         Show output in the process.\n  -V, --version         Show version info and exit.\n  --help                Show this message and exit.\n```\n\n## Miscellany\n\n* A retry mechanism (via pypi `tenacity`) is built-in to fetch info from glosbe. Refer to the source file for details.\n* Local cache (via pypi `joblib`) is used so that you can interrupt anytime and continue later.\n* Scraping is often frowned upon and sometimes can result in your IP being banned from the website. Use this package at your own discretion.\n",
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/scrape-glosbe-dict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
