# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nylondetector',
 'nylondetector.crawling',
 'nylondetector.inference',
 'nylondetector.modeling',
 'nylondetector.preprocess',
 'nylondetector.util',
 'nylondetector.vis']

package_data = \
{'': ['*'],
 'nylondetector.crawling': ['data/blog/백내장+부수입/url_original/*',
                            'data/blog/백내장+소개/url_original/*',
                            'data/blog/백내장+수당/url_original/*',
                            'data/blog/백내장+숙소/url_original/*',
                            'data/blog/백내장+실비/url_original/*',
                            'data/blog/백내장+실손/url_original/*',
                            'data/blog/백내장+페이백/url_original/*',
                            'data/blog/백내장+할인/url_original/*',
                            'data/blog/백내장+호텔/url_original/*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'baram>=0.1.0,<0.2.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'fire>=0.4.0,<0.5.0',
 'nest-asyncio>=1.5.5,<2.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'ujson>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'nylondetector',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Kwangsik Lee',
    'author_email': 'lks21c@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
