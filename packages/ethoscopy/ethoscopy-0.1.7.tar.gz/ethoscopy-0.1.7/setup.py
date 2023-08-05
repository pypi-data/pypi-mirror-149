# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ethoscopy', 'ethoscopy.misc']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'pandas>=1.4.2,<2.0.0', 'plotly>=5.7.0,<6.0.0']

setup_kwargs = {
    'name': 'ethoscopy',
    'version': '0.1.7',
    'description': 'A python based toolkit to download and anlyse data from the Ethoscope hardware system.',
    'long_description': "**ethoscopy**\n\nA data-analysis toolbox utilising the python language for use with data collected from 'Ethoscopes', a Drosophila video monitoring system.\n\nFor more information on the ethoscope system: https://www.notion.so/The-ethoscope-60952be38787404095aa99be37c42a27\n\nEthoscopy is made to work alongside this system, working as a post experiment analysis toolkit. \n\nEthoscopy provides the tools to download epxerimental data from a remote ftp servers as setup in ethoscope tutorial above. Downloaded data can be curated during the pipeline in a range of ways, all fromatted using the pandas data structure.\n\nFurther the ethoscopy package provides behavpy a subclassed version of pandas that combines metadata with the data for easily manipulation.\n\n**TO COME** In addtion the behavpy class has hmmlearn imbedded, a python package for the use of hidden markov models (HMM) (https://hmmlearn.readthedocs.io/en/latest/). Here you can set the architecture and train a HMM of your choice. There are several plotting functions avaiable alongside side it to explore the hidden markov model, using plotly as graphing tool of choice.\n",
    'author': 'Blackhurst Laurence',
    'author_email': 'l.blackhurst19@imperial.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.11',
}


setup(**setup_kwargs)
