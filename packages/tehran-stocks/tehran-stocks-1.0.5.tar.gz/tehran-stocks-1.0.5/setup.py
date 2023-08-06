# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tehran_stocks',
 'tehran_stocks.config',
 'tehran_stocks.download',
 'tehran_stocks.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'SQLAlchemy>=1.4.28,<2.0.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'jalali-pandas>=0.2.0,<0.3.0',
 'lxml>=4.8.0,<5.0.0',
 'pandas>=1.3.5,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'tehran-stocks',
    'version': '1.0.5',
    'description': 'Data Downloader for Tehran stock market',
    'long_description': "# Tehran Stock Market بورس تهران در پایتون\n\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/tehran_stocks.svg?color=blue)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/tehran_stocks.svg?color=blue)\n[![PyPI version](https://badge.fury.io/py/tehran-stocks.svg)](https://badge.fury.io/py/tehran-stocks)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tehran-stocks.svg)\n[![HitCount](https://hits.dwyl.com/ghodsizadeh/tehran-stocks.svg?style=flat-square)](http://hits.dwyl.com/ghodsizadeh/tehran-stocks)\n[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ghodsizadeh/tehran-stocks/blob/master/Example/Read_Data.ipynb)\n\nA python package that helps to access TSETMC stock price history, Using OOP Interface\n\n## Features\n\n- Download All stocks prices\n- Download prices from a group (i.e ETFs or cars, etc.)\n- Download Price history of one specific Stock\n- After first setup available offline.\n- CommandLine Interface\n- Export data to csv, excel or Stata(dta)\n- Compatible with `sqlalchemy`\n- Compatible with `PANDAS`\n- Based on light `sqlite`\n\n---\n\n## Table of Contents\n\n<!-- TOC orderedlist:true -->\n\n- [1. Tehran Stock Market بورس تهران در پایتون](#1-tehran-stock-market-%D8%A8%D9%88%D8%B1%D8%B3-%D8%AA%D9%87%D8%B1%D8%A7%D9%86-%D8%AF%D8%B1-%D9%BE%D8%A7%DB%8C%D8%AA%D9%88%D9%86)\n    - [1.1. Features](#11-features)\n    - [1.2. Table of Contents](#12-table-of-contents)\n- [2. Usage](#2-usage)\n    - [2.1. - Install](#21---install)\n    - [2.2. - Initialization](#22---initialization)\n        - [2.2.1. -1 Command line](#221--1-command-line)\n        - [2.2.2. -2 Python](#222--2-python)\n    - [2.3. - Download and Update prices](#23---download-and-update-prices)\n        - [2.3.1. -1 Command line](#231--1-command-line)\n        - [2.3.2. -2 Python](#232--2-python)\n    - [2.4. - Access Data](#24---access-data)\n        - [2.4.1. -1 Search Stocks](#241--1-search-stocks)\n        - [2.4.2. -2 Get Instant price and more details:](#242--2-get-instant-price-and-more-details)\n    - [2.5. - Custom Database](#25---custom-database)\n    - [2.6. Todo](#26-todo)\n- [3. Support❤️](#3-support)\n\n<!-- /TOC -->\n\n# Usage\n\n## 0 - Install\n\n```bash\npip install tehran_stocks\n```\n\n## 1- Initialization\n\nFor first use you need initialize the database\n\n### 1-1 Command line\n\n```bash\nts-get init  # Set up to sqlite database\n```\n\n### 1-2 Python\n\n```python\nimport tehran_stocks\n# On first import package initialize itself\n```\n\nDuring initialization you will prompt for downloading all prices. if you answer yes it will download all prices, otherwise you can download data\n\n## 2- Download and Update prices\n\n### 2-1 Command line\n\n```bash\nts-get update # update  all price , or download all if no price exist\nts-get  group 34 ## 34 is the code for car's group.\nts-get get_groups ## get group name and group codes\n```\n\n### 2-2 Python\n\n```python\nfrom tehran_stocks import get_all_price, Stocks, update_group\n\nget_all_price() # download and(or) update all prices\n\nupdate_group(34) #download and(or) update Stocks in groupCode = 34 (Cars)\n\nStocks.get_group() # to see list of group codes\n```\n\n## 3- Access Data\n\nTo access data you can use `Stocks` which is an customized `sqlalchemy` object, which helps you to find prices on an easy way.\n\n### 3-1 Search Stocks\n\n```python\nfrom tehran_stocks import Stocks, db\n\n# You can use query to find stocks\nstock = Stocks.query.filter_by(name='كگل').first() #find by symbol(نماد)\n\nstock = Stocks.query.filter_by(code='35700344742885862').first() # find by code on tsetmc url\n\nstock = Stocks.query.filter(Stocks.title.like('%گل گهر%')).first() # Search by title\n\nstock_list = Stocks.query.filter_by(group_code =34).all() # find all Stocks in Khodro\n\nstock_list = Stocks.query.filter(Stocks.group_code.in_([13,34])).all() # all stocks in khodro and felezat\n\n\n## (Advanced)or run sql query using orm or raw sql\ndb.session.query(Stocks.group_code, Stocks.group_name).group_by(Stocks.group_code).all()\n\ndb.session.execute('select group_code , group_name from stocks group by group_name').fetchall()\n```\n\nNow easily access stock price and do whatever you want with `pandas` dataframes:\n\n```python\n# use data as a pandas dataframe\n>>> stock.df#\n      id               code        ticker  dtyyyymmdd    first     high      low    close        value      vol  openint per     open     last       date\n0  22491  35700344742885862  Gol-E-Gohar.    20040829  12000.0  12021.0  12000.0  12000.0  18841605000  1570000     2708   D  12000.0  12000.0 2004-08-29\n\n>>> stock.summary()\nStart date: 2004/08/29\nEnd date: 2019/07/14\nTotal days: 2987\n\n>>> stock.update()\n# update stock price history\n\n# Export to your preferred format\n>>> stock.df.to_csv('price.csv')\n>>> stock.df.to_excel('price.xlsx')\n>>> stock.df.to_stata('price.dta')\n\n```\n\n### 3-2 Get Instant price and more details:\n\n```python\n>>> stock.get_instant_detail()\n{'time': '12:29:57',\n 'last_price': '12950',\n 'last_close': '13060',\n 'last_high': '13300',\n 'last_low': '13130',\n 'last_open': '13330',\n 'trade_count': '12760',\n 'trade_volume': '1140',\n 'trade_value': '4671236',\n 'market_cap': '60715047900',\n 'date_string': '20220404',\n 'time_string': '122957'}\n\n# get change in share count\n>>> stock.get_shares_history()\n\ndate\tnew_shares\told_shares\tgdate\n0\t1400-12-08 00:00:00\t200.000 B\t100.000 B\t2022-02-27\n1\t1400-04-20 00:00:00\t100.000 B\t74.400 B\t2021-07-11\n\n# get change in price ~ dividend, split, etc.\n>> stock.get_dividend()\ndate\tafter\tbefore\tdividend\tgdate\n0\t1400-04-16 00:00:00\t18770\t20070\t1300\t2021-07-07\n1\t1399-04-18 00:00:00\t16350\t17250\t900\t2020-07-08\n)\n```\n\n## 4- Custom Database\n\nYou can change the default database by updating the config file on:\n\n```bash\n~/.tse/config.yml #unix MacOS/Linux\nC:\\Users\\User\\{USERNAME}\\.tse\\config.yml #Windows\n```\n\nCustom Config for postgresql (you may need to install `pyscopg2`):\n\n```yaml\ndatabase:\n  database: stocks\n  engine: postgresql\n  host: localhost\n  password: password\n  port: 5432\n  user: postgres\n```\n\n## Todo\n\n- [x] Create Database\n- [x] Download Data\n- [x] CommandLine Support\n- [x] Jalali Support\n- [x] Instant Data\n- [x] Custom database\n\n# Support❤️\n\n- If you like this package you can buy me a cup of coffee ☕️.\n  - [IDPAY](https://idpay.ir/ghodsizadeh)\n  - ![Keybase BTC](https://img.shields.io/keybase/btc/mghodsizadeh)\n- Subscribe and share my youtube channel [![Youtube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com/channel/UCF3v_GwH3Jg2c-V3hRwmcbg)\n",
    'author': 'Mehdi Ghodsizadeh',
    'author_email': 'mehdi.ghodsizadeh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ghodsizadeh.github.io/tehran-stocks/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
