# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_parser']

package_data = \
{'': ['*'], 'beancount_parser': ['grammar/*']}

install_requires = \
['lark>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'beancount-parser',
    'version': '0.1.21',
    'description': 'Standalone Lark based Beancount syntax parser (not relying on Beancount library), MIT license',
    'long_description': '# beancount-parser [![CircleCI](https://circleci.com/gh/LaunchPlatform/beancount-parser/tree/master.svg?style=svg)](https://circleci.com/gh/LaunchPlatform/beancount-parser/tree/master)\nStandalone [Lark](https://github.com/lark-parser/lark) LALR(1) based Beancount syntax parser (not relying on Beancount library), MIT license\n\nPlease also checkout out [beancount-black](https://github.com/LaunchPlatform/beancount-black), an opinionated beancount code formatter based on beancount-parser.\n\n## Features\n\n- **MIT licensed** - the only dependency is [Lark](https://github.com/lark-parser/lark)\n- **Extremely fast** - LALR(1) is used\n- **Section awareness** - mac org symbol mark `*` will be parsed\n- **Comment awareness** - comments will be parsed\n- **Not a validator** - it does not validate beancount syntax, invalid beancount syntax may still pass the parsing\n\n# Sponsor\n\nThe original project beancount-parser was meant to be an internal tool built by [Launch Platform LLC](https://launchplatform.com) for \n\n<p align="center">\n  <a href="https://beanhub.io"><img src="https://github.com/LaunchPlatform/beancount-black/raw/master/assets/beanhub.svg?raw=true" alt="BeanHub logo" /></a>\n</p>\n\nA modern accounting book service based on the most popular open source version control system [Git](https://git-scm.com/) and text-based double entry accounting book software [Beancount](https://beancount.github.io/docs/index.html).\nWe realized adding new entries with BeanHub automatically over time makes beancount file a mess.\nSo obviously, a strong code formatter.\nAnd to deal with comments and other corner cases, it\'s easier to build a parser from ground up without relying on Beancount.\nWhile SaaS businesses won\'t be required to open source an internal tool like this, we still love that the service is only possible because of the open-source tool we are using.\nWe think it would be greatly beneficial for the community to access a tool like this, so we\'ve decided to open source it under MIT license, hope you find this tool useful 😄\n\n## Install\n\nTo install the parser, simply run\n\n```bash\npip install beancount-parser\n```\n\n## Usage\n\nIf you want to run the parse beancount code, you can do this\n\n```python\nimport io\n\nfrom beancount_parser.parser import make_parser\n\nparser = make_parser()\ntree = parser.parse(beancount_content)\n# do whatever you want with the tree here\n```\n\n## Feedbacks\n\nFeedbacks, bugs reporting or feature requests are welcome 🙌, just please open an issue.\nNo guarantee we have time to deal with them, but will see what we can do.\n',
    'author': 'Fang-Pen Lin',
    'author_email': 'fangpen@launchplatform.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LaunchPlatform/beancount-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
