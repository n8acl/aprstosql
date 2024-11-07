import pymssql # SQL Server
import pymysql # MySQL
import sqlalchemy
from sqlalchemy import text as sqltext
import json
import os
from os import system

def db_connection(): 
    #############################
    # import config json file For Database connection variables

    config_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config.json'))

    with open(config_file, "r") as read_file:
        cfg = json.load(read_file)

    # define SQL connection variables

    sql_host = cfg['database']['credentials']['host']
    sql_user = cfg['database']['credentials']['username']
    sql_password = cfg['database']['credentials']['password']
    sql_database = 'APRS'

    ## Create Engine Object

    if cfg['database']['rdbms_type'] == 'mssql': # SQL Server
        db_uri = 'mssql+pymssql://{0}:{1}@{2}/{3}'.format(sql_user, sql_password, sql_host, sql_database)

    else: # MySQL/MariaDB
        db_uri = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(sql_user, sql_password, sql_host, sql_database)
      
    
    return sqlalchemy.create_engine(db_uri)