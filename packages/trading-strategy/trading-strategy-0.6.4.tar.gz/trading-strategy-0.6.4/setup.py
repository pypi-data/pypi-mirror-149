# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradingstrategy',
 'tradingstrategy.analysis',
 'tradingstrategy.environment',
 'tradingstrategy.frameworks',
 'tradingstrategy.transport',
 'tradingstrategy.utils']

package_data = \
{'': ['*'],
 'tradingstrategy': ['chains/*',
                     'chains/.ci/*',
                     'chains/.github/*',
                     'chains/.github/ISSUE_TEMPLATE/*',
                     'chains/.github/workflows/*',
                     'chains/_data/chains/*',
                     'chains/_data/chains/deprecated/*',
                     'chains/_data/icons/*',
                     'chains/gradle/wrapper/*',
                     'chains/src/main/kotlin/org/ethereum/lists/chains/*',
                     'chains/src/main/kotlin/org/ethereum/lists/chains/model/*',
                     'chains/src/test/kotlin/org/ethereum/lists/chains/*',
                     'chains/src/test/resources/test_chains/invalid/*',
                     'chains/src/test/resources/test_chains/invalid/explorerinvalidurl/*',
                     'chains/src/test/resources/test_chains/invalid/explorermissingurl/*',
                     'chains/src/test/resources/test_chains/invalid/explorernoname/*',
                     'chains/src/test/resources/test_chains/invalid/explorersnotarray/*',
                     'chains/src/test/resources/test_chains/invalid/sameshortname/*',
                     'chains/src/test/resources/test_chains/invalid/withparentchaindoesnotexist/*',
                     'chains/src/test/resources/test_chains/invalid/withparentextrabridgeelementnoobject/*',
                     'chains/src/test/resources/test_chains/invalid/withparentextrabridgesfield/*',
                     'chains/src/test/resources/test_chains/invalid/withparentextrabridgesnoarray/*',
                     'chains/src/test/resources/test_chains/invalid/withparentextrafield/*',
                     'chains/src/test/resources/test_chains/invalid/withparentinvalidtype/*',
                     'chains/src/test/resources/test_chains/invalid/withparentnobject/*',
                     'chains/src/test/resources/test_chains/invalid/wrongexplorerstandard/*',
                     'chains/src/test/resources/test_chains/valid/*',
                     'chains/src/test/resources/test_chains/valid/withexplorer/*',
                     'chains/src/test/resources/test_chains/valid/withparent/*',
                     'chains/src/test/resources/test_chains/valid/withparentbridge/*']}

install_requires = \
['chart-studio>=1.1.0,<2.0.0',
 'cufflinks>=0.17.3,<0.18.0',
 'dataclasses-json>=0.5.4,<0.6.0',
 'eth-hash[pycryptodome]>=0.3.1,<0.4.0',
 'eth-utils>=1.10.0,<2.0.0',
 'mplfinance>=0.12.7-alpha.17,<0.13.0',
 'pandas>=1.3.5,<2.0.0',
 'plotly>=5.1.0,<6.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'scipy>=1.8.0,<2.0.0',
 'tqdm>=4.61.2,<5.0.0',
 'trading-strategy-backtrader>=0.1,<0.2']

extras_require = \
{':extra == "qstrader"': ['trading-strategy-qstrader[qstrader]>=0.5.0,<0.6.0']}

setup_kwargs = {
    'name': 'trading-strategy',
    'version': '0.6.4',
    'description': 'Algorithmic trading and quantitative financial analysis framework for decentralised exchanges and blockchains',
    'long_description': '[![CI Status](https://github.com/tradingstrategy-ai/trading-strategy/actions/workflows/python-app.yml/badge.svg)](https://github.com/tradingstrategy-ai/trading-strategy/actions/workflows/python-app.yml)\n\n[![pip installation works](https://github.com/tradingstrategy-ai/trading-strategy/actions/workflows/pip-install.yml/badge.svg)](https://github.com/tradingstrategy-ai/trading-strategy/actions/workflows/pip-install.yml)\n\n[![Trading Strategy logo](https://hv4gxzchk24cqfezebn3ujjz6oy2kbtztv5vghn6kpbkjc3vg4rq.arweave.net/n8pMe2r9Wv3oQsPk4Swie55CZLgXWuExDsBOtczNdCY)](https://tradingstrategy.ai)\n\n# Trading Strategy framework for Python\n\nTrading Strategy framework is a Python framework for algorithmic trading on decentralised exchanges. \nIt is using [backtesting data](https://tradingstrategy.ai/trading-view/backtesting) and [real-time price feeds](https://tradingstrategy.ai/trading-view)\nfrom [Trading Strategy Protocol](https://tradingstrategy.ai/). \n\n# Use cases\n\n* Analyse cryptocurrency investment opportunities on [decentralised exchanges (DEXes)](https://tradingstrategy.ai/trading-view/exchanges)\n\n* Creating trading algorithms and trading bots that trade on DEXes\n\n* Deploy trading strategies as on-chain smart contracts where users can invest and withdraw with their wallets\n\n# Features\n\n* Supports multiple blockchains like [Ethereum mainnet](https://tradingstrategy.ai/trading-view/ethereum), [Binance Smart Chain](https://tradingstrategy.ai/trading-view/binance) and [Polygon](https://tradingstrategy.ai/trading-view/polygon)\n\n* Access trading data from on-chain decentralised exchanges like [SushiSwap](https://tradingstrategy.ai/trading-view/ethereum/sushiswap), [QuickSwap](https://tradingstrategy.ai/trading-view/polygon/quickswap) and [PancakeSwap](https://tradingstrategy.ai/trading-view/binance/pancakeswap-v2)\n\n* Integration with [Jupyter Notebook](https://jupyter.org/) for easy manipulation of data \n\n* Utilise Python quantita frameworks like [Backtrader](https://github.com/tradingstrategy-ai/backtrader) and [QSTrader](https://github.com/tradingstrategy-ai/qstrader) to create, analyse and backtest DEX trading algorithms \n\n# Example and getting started \n\nSee [the Getting Started notebook](https://tradingstrategy.ai/docs/programming/examples/getting-started.html) and the rest of the [Trading Strategy documentation](https://tradingstrategy.ai/docs/).\n\n# Prerequisites\n\nPython 3.9+\n\n# Installing the package\n\n**Note**: Unless you are an experienced Python developer, [the suggested usage of Trading Algorithm framework is using Google Colab hosted environments](https://tradingstrategy.ai/docs/programming/examples/getting-started.html).\n\nYou can install this package with `poetry` or `pip`\n\n```shell\npoetry add trading-strategy\n```\n\n\n```shell\npip install trading-strategy \n```\n\nFor [QSTrader](https://pypi.org/project/trading-strategy-qstrader/) based trading algorithm support you need to install the related optional dependencies:\n\n```shell\npoetry add trading-strategy[qstrader]\n```\n\n# Documentation\n\n[Read documentation online](https://tradingstrategy.ai/docs/).\n\nCommunity\n---------\n\n* [Trading Strategy website](https://tradingstrategy.ai)\n\n* [Blog](https://tradingstrategy.ai/blog)\n\n* [Twitter](https://twitter.com/TradingProtocol)\n\n* [Discord](https://tradingstrategy.ai/community#discord) \n\n* [Telegram channel](https://twitter.com/TradingProtocol)\n\n* [Changelog and version history](https://github.com/tradingstrategy-ai/trading-strategy/blob/master/CHANGELOG.md)\n\n\n[Read more documentation how to develop this package](https://tradingstrategy.ai/docs/programming/development.html).\n\n# License\n\nGNU AGPL 3.0. \n',
    'author': 'Mikko Ohtamaa',
    'author_email': 'mikko@tradingstrategy.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tradingstrategy.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
