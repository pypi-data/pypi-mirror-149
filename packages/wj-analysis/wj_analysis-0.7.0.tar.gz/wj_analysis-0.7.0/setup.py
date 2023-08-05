# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wj_analysis',
 'wj_analysis.common',
 'wj_analysis.digital_med',
 'wj_analysis.facebook',
 'wj_analysis.facebook_insights',
 'wj_analysis.instagram',
 'wj_analysis.reach_fb_ig',
 'wj_analysis.twitter',
 'wj_analysis.unit_test']

package_data = \
{'': ['*'], 'wj_analysis.common': ['stopwords/*']}

install_requires = \
['nltk>=3.7,<4.0',
 'numpy==1.17.4',
 'pandas==0.25.3',
 'scikit-learn>=1.0.2,<2.0.0',
 'spacy>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'wj-analysis',
    'version': '0.7.0',
    'description': 'Whale&Jaguar Libary - Analysis',
    'long_description': None,
    'author': 'Sebastian Franco',
    'author_email': 'jsfranco@whaleandjaguar.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7.1,<4.0',
}


setup(**setup_kwargs)
