# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['behave_db', 'behave_db.steps']

package_data = \
{'': ['*']}

install_requires = \
['JayDeBeApi>=1.2.3,<2.0.0', 'Jinja2>=2.5,<3.0', 'behave>=1.2.6,<2.0.0']

setup_kwargs = {
    'name': 'behave-db',
    'version': '0.0.3',
    'description': 'BDD DB steps implementation for Behave',
    'long_description': '# behave-db\nBDD DB steps implementation for Behave\n\n_behave-db_ is a db testing tools for\nBehavior-Driven-Development, based on\n[behave](http://pypi.python.org/pypi/behave) and\n[JayDeBeApi](https://github.com/baztian/jaydebeapi).\n\n\n## Hello world (TODO)\n\n\n',
    'author': 'zmr',
    'author_email': 'zmr_01@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/M-halliday/behave-db',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
