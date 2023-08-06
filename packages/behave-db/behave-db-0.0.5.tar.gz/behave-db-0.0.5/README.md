# behave-db
BDD DB steps implementation for Behave

_behave-db_ is a db testing tools for
Behavior-Driven-Development, based on
[behave](http://pypi.python.org/pypi/behave) and
[JayDeBeApi](https://github.com/baztian/jaydebeapi).



## Installation 

You can get and install behave-db with pip

```
$ pip install  behave-db
```

## Usage example

*yourapp/features/environment.py*:

```python
from behave_db import environment as benv

def before_all(context):
    import behave_db
    config_datas = {}
    #jdbc-drivers in data_dir
    data_dir = os.path.join(
        os.path.dirname(behave_db.__file__), "../../tests/data"
    )
    #set csv-jdbc-config
    config_datas['driver_name'] = "org.relique.jdbc.csv.CsvDriver"
    config_datas['driver_jar_path'] = os.path.join(data_dir,"drivers","csvjdbc-1.0-37.jar")
    config_datas['csv_jdbc_url'] = "jdbc:relique:csv:" + data_dir
    config_datas['db_user'] = None
    config_datas['db_password'] = None
    #copy var to behave_db
    benv.before_all(context)
    context.db_config = config_datas


def after_scenario(context, scenario):
    # auto close connect
    context.execute_steps(u"""
                 When I close the connect
                """)

```

*yourapp/features/steps/some\_db\_stuff.py*:

```python
from behave_db.steps import *
```

*yourapp/features/some\_db.feature*:

```gherkin
Feature: databases testing
    testing behave-db steps

    Scenario: connect to csv with var 
        Given I connect to db "$csv_jdbc_url" with user "$db_user" and password "$db_password"
        When I wait for 1 seconds
        Then I set "count_num" from the search with "SELECT count(1) FROM csv_datas "
        And  the "$count_num" is not null
        And  the "$count_num" value should be "200"

```

*yourapp/data/some\_db_jdbc.jar*:

```shell
$ ls

csvjdbc-1.0-37.jar
...
...

```

*run in yourapp/*:

``` python
# run behave in yourapp dir

E:\git-code\behave-db\tests>behave

Feature: databases testing # features/basic.feature:1
  testing behave-db steps
  Scenario: connect to csv with var                                                        # features/basic.feature:4
    Given I connect to db "$csv_jdbc_url" with user "$db_user" and password "$db_password" # ../src/behave_db/steps/basic.py:12
    When I wait for 1 seconds                                                              # ../src/behave_db/steps/basic.py:53
    Then I set "count_num" from the search with "SELECT count(1) FROM csv_datas "          # ../src/behave_db/steps/basic.py:59
    And the "$count_num" is not null                                                       # ../src/behave_db/steps/basic.py:68
    And the "$count_num" value should be "200"                                             # features/steps/steps.py:8

1 feature passed, 0 failed, 0 skipped
1 scenarios passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m1.797s

```

## other tools on behave

*web application testing*

[behaving](https://github.com/ggozad/behaving)

*api testing*

[behave-http](https://github.com/mikek/behave-http)


