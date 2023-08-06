# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'xepmts', 'xepmts.db', 'xepmts.streams']

package_data = \
{'': ['*']}

install_requires = \
['click',
 'eve-panel>=0.3.27,<0.4.0',
 'toml>=0.10.2,<0.11.0',
 'xeauth>=0.1.19,<0.2.0',
 'xepmts-endpoints>=0.1.4,<0.2.0']

extras_require = \
{':extra == "live" or extra == "full"': ['streamz'],
 'full': ['hvplot>=0.7.0,<0.8.0', 'dask[dataframe]>=2021.2.0,<2022.0.0'],
 'plotting': ['hvplot>=0.7.0,<0.8.0']}

entry_points = \
{'console_scripts': ['xepmts = xepmts.cli:main']}

setup_kwargs = {
    'name': 'xepmts',
    'version': '0.5.9',
    'description': 'Python client for accessing the XENON experiment PMT data.',
    'long_description': '======\nxepmts\n======\nA helper package for managing the PMT database used by the XENONnT Dark Matter Experiment.\n\n.. image:: https://img.shields.io/pypi/v/xepmts.svg\n        :target: https://pypi.python.org/pypi/xepmts\n\n.. image:: https://img.shields.io/travis/jmosbacher/xepmts.svg\n        :target: https://travis-ci.com/jmosbacher/xepmts\n\n.. image:: https://readthedocs.org/projects/xepmts/badge/?version=latest\n        :target: https://xepmts.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\nBasic Usage\n-----------\n\n.. code-block:: python\n\n    import xepmts\n\n    # If you are using a notebook:\n    xepmts.notebook()\n\n    # use v1 client\n    db = xepmts.login("v1", token=\'YOUR-API-TOKEN\')\n\n    # or the v2 client\n    db = xepmts.login("v2")\n\n    # set the number of items to pull per page\n    db.tpc.installs.items_per_page = 25\n    \n    # get the next page \n    page = db.tpc.installs.next_page()\n\n    # iterate over pages:\n    for page in db.tpc.installs.pages():\n        df = page.df\n        # do something with data\n\n    # select only top array\n    top_array = db.tpc.installs.filter(array="top")\n\n    # iterate over top array pages\n    for page in top_array.pages():\n        df = page.df\n        # do something with data\n\n    query = dict(pmt_index=4)\n    # get the first page of results for this query as a list of dictionaries\n    docs = db.tpc.installs.find(query, max_results=25, page_number=1)\n\n    # same as find, but returns a dataframe \n    df = db.tpc.installs.find_df(query)\n\n\n    # insert documents into the database\n    docs = [{"pmt_index": 1, "position_x": 0, "position_y": 0}]\n    db.tpc.installs.insert_documents(docs)\n    \n* Free software: MIT\n* Documentation: https://xepmts.readthedocs.io/\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/xepmts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
