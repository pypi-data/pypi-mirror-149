# -*- coding: UTF-8 -*-  
from __future__ import unicode_literals
import time
import jaydebeapi
import json

from behave import step
from behave_db.utils import db_config_vars



@step(u'I connect to db "{jdbc_url}" with user "{db_user}" and password "{db_password}"')
@db_config_vars
def conn_to_databases(context, db_user, db_password, jdbc_url):
    # get driver_name and jar by db_config
    driver_name = context.db_config["driver_name"]
    driver_jar_path =  context.db_config["driver_jar_path"]
    OAuth = return_OAuth(context, db_user, db_password)
    #conn to db by jaydebeapi
    context.conn = jaydebeapi.connect(driver_name,
                              jdbc_url,
                              OAuth,
                              driver_jar_path)


@step(u'I connect to db with json')
@db_config_vars
def conn_to_databases_with_json(context):
    # get driver_name and jar from context.text
    text_datas = json.loads(context.text)
    OAuth = return_OAuth(context, text_datas["db_user"], text_datas["db_password"])
    #conn to db by jaydebeapi
    context.conn = jaydebeapi.connect(text_datas["driver_name"],
                              text_datas["jdbc_url"],
                              OAuth,
                              text_datas["driver_jar_path"])


def return_OAuth(context, username, passwd):
    # sqlite/csv need't password, process user and password
    OAuth = [username,passwd]
    if not username and not passwd:
        OAuth = None
    return OAuth


@step(u'I close the connect')
@db_config_vars
def close_connect_db(context):
    context.conn.close()


@step(u'I wait for {timeout:d} seconds')
@db_config_vars
def wait_for_timeout(context, timeout):
    time.sleep(timeout)


@step(u'I set "{key}" from the search with "{sql}"')
@db_config_vars
def set_var_from_search_sql(context, key, sql):
    with context.conn.cursor() as curs:
        curs.execute(sql)
        sql_result = curs.fetchall()
    context.db_config[key] = sql_result


@step(u'the "{result}" is not null')
@db_config_vars
def result_is_not_null(context, result):
    assert result, u'The result is null'


@step(u'the "{result}" is null')
@db_config_vars
def result_is_null(context, result):
    assert result is None, u'The result is not null'

