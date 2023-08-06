# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eve_panel', 'eve_panel.auth', 'tests', 'tests.test_app']

package_data = \
{'': ['*']}

install_requires = \
['eve>=1.1.3,<2.0.0', 'httpx>=0.19,<0.20', 'numpy', 'panel>=0.13.0,<0.14.0']

extras_require = \
{'full': ['hvplot'], 'plotting': ['hvplot']}

setup_kwargs = {
    'name': 'eve-panel',
    'version': '0.3.28',
    'description': 'Top-level package for Eve-Panel.',
    'long_description': '=========\nEve-Panel\n=========\n\n\n.. image:: https://img.shields.io/pypi/v/eve_panel.svg\n        :target: https://pypi.python.org/pypi/eve_panel\n\n.. image:: https://img.shields.io/travis/jmosbacher/eve_panel.svg\n        :target: https://travis-ci.com/jmosbacher/eve_panel\n\n.. image:: https://readthedocs.org/projects/eve-panel/badge/?version=latest\n        :target: https://eve-panel.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\nDynamically create an httpx based client for any Eve api. Uses Param + Cerberus for type enforcement and Panel for GUIs.\nThis is just a prototype package,features will slowly be added as i need them for my own purposes.\nThe api is expected to change without warning based on my needs but feel free to fork or copy parts and adapt to your own needs.\n\nTo view the widgets in a notebook you will need to install the pyviz plugin. For details, see panel docs.\n\nUsage\n-----\n\n.. code-block:: python\n\n    import eve\n    from eve_panel import EveClient\n\n\n    app = eve.Eve()\n\n    api = eve_panel.EveClient.from_app(app)\n    \n    # optional\n    api.set_token("my-secret-token")\n\n    # show a resources gui\n    api.resource_name\n\n    # get a specific item\n    api.resource_name["item_id"]\n\n    # get current page\n    api.resource_name.current_page()\n\n    # get next page\n    api.resource_name.next_page()\n\n    # get previous page\n    api.resource_name.previous_page()\n\n    # insert new documents\n    docs = [{"name": "new document"}]\n    api.resource_name.insert_documents(docs)\n    \n\n\n* Free software: MIT\n* Documentation: https://eve-panel.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jmosbacher.github.io/eve-panel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
