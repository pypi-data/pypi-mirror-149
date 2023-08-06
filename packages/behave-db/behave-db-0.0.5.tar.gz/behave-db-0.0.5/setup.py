# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['behave_db', 'behave_db.steps']

package_data = \
{'': ['*']}

install_requires = \
['JayDeBeApi>=1.2.3,<2.0.0', 'behave>=1.2.6,<2.0.0']

setup_kwargs = {
    'name': 'behave-db',
    'version': '0.0.5',
    'description': 'BDD DB steps implementation for Behave',
    'long_description': '# behave-db\nBDD DB steps implementation for Behave\n\n_behave-db_ is a db testing tools for\nBehavior-Driven-Development, based on\n[behave](http://pypi.python.org/pypi/behave) and\n[JayDeBeApi](https://github.com/baztian/jaydebeapi).\n\n\n\n## Installation \n\nYou can get and install behave-db with pip\n\n```\n$ pip install  behave-db\n```\n\n## Usage example\n\n*yourapp/features/environment.py*:\n\n```python\nfrom behave_db import environment as benv\n\ndef before_all(context):\n    import behave_db\n    config_datas = {}\n    #jdbc-drivers in data_dir\n    data_dir = os.path.join(\n        os.path.dirname(behave_db.__file__), "../../tests/data"\n    )\n    #set csv-jdbc-config\n    config_datas[\'driver_name\'] = "org.relique.jdbc.csv.CsvDriver"\n    config_datas[\'driver_jar_path\'] = os.path.join(data_dir,"drivers","csvjdbc-1.0-37.jar")\n    config_datas[\'csv_jdbc_url\'] = "jdbc:relique:csv:" + data_dir\n    config_datas[\'db_user\'] = None\n    config_datas[\'db_password\'] = None\n    #copy var to behave_db\n    benv.before_all(context)\n    context.db_config = config_datas\n\n\ndef after_scenario(context, scenario):\n    # auto close connect\n    context.execute_steps(u"""\n                 When I close the connect\n                """)\n\n```\n\n*yourapp/features/steps/some\\_db\\_stuff.py*:\n\n```python\nfrom behave_db.steps import *\n```\n\n*yourapp/features/some\\_db.feature*:\n\n```gherkin\nFeature: databases testing\n    testing behave-db steps\n\n    Scenario: connect to csv with var \n        Given I connect to db "$csv_jdbc_url" with user "$db_user" and password "$db_password"\n        When I wait for 1 seconds\n        Then I set "count_num" from the search with "SELECT count(1) FROM csv_datas "\n        And  the "$count_num" is not null\n        And  the "$count_num" value should be "200"\n\n```\n\n*yourapp/data/some\\_db_jdbc.jar*:\n\n```shell\n$ ls\n\ncsvjdbc-1.0-37.jar\n...\n...\n\n```\n\n*run in yourapp/*:\n\n``` python\n# run behave in yourapp dir\n\nE:\\git-code\\behave-db\\tests>behave\n\nFeature: databases testing # features/basic.feature:1\n  testing behave-db steps\n  Scenario: connect to csv with var                                                        # features/basic.feature:4\n    Given I connect to db "$csv_jdbc_url" with user "$db_user" and password "$db_password" # ../src/behave_db/steps/basic.py:12\n    When I wait for 1 seconds                                                              # ../src/behave_db/steps/basic.py:53\n    Then I set "count_num" from the search with "SELECT count(1) FROM csv_datas "          # ../src/behave_db/steps/basic.py:59\n    And the "$count_num" is not null                                                       # ../src/behave_db/steps/basic.py:68\n    And the "$count_num" value should be "200"                                             # features/steps/steps.py:8\n\n1 feature passed, 0 failed, 0 skipped\n1 scenarios passed, 0 failed, 0 skipped\n5 steps passed, 0 failed, 0 skipped, 0 undefined\nTook 0m1.797s\n\n```\n\n## other tools on behave\n\n*web application testing*\n\n[behaving](https://github.com/ggozad/behaving)\n\n*api testing*\n\n[behave-http](https://github.com/mikek/behave-http)\n\n\n',
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
