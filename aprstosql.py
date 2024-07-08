#!/usr/bin/env python3

#################################################################################

# APRStoSQL
# Developed by: Jeff Lehman, N8ACL
# Current Version: 07032024
# https://github.com/n8acl/aprstosql

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Discord: Ravendos
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

###################   DO NOT CHANGE BELOW   #########################

################################
# Import Libraries

import json
import aprslib
import pymssql
import sqlalchemy
from sqlalchemy import text as sqltext
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists, create_database
from time import sleep

import src.create_database as cdb

#############################
# import config json file

with open("config.json", "r") as read_file:
    config = json.load(read_file)


############################################################################
##  SQL Server Connection creation

# define SQL Server connection variables
sql_host = config['mssql']['host']
sql_user = config['mssql']['username']
sql_password = config['mssql']['password']
sql_database = 'APRS'
sql_driver = "{ODBC+Driver+18+for+SQL+Server}"

# configure SQL Server Database connection with SQL Alchemy
db_engine = sqlalchemy.create_engine('mssql+pymssql://{0}:{1}@{2}/{3}'.
                                               format(sql_user, sql_password, 
                                                      sql_host, sql_database))


if not database_exists(db_engine.url):
        print("Error Connecting to Database. Does not exist. Creating database....")
        new_engine = sqlalchemy.create_engine('mssql+pymssql://{0}:{1}@{2}/{3}'.
                                                   format(sql_user, sql_password, 
                                                          sql_host, 'master'))
        
        with new_engine.connect() as con:
            create_database(db_engine.url)
            cdb.create_db(con)


################################################################
## Define Variables
linefeed = "\n"
callsign = config['callsign']
port = 14580
passcode = aprslib.passcode(callsign)
set_filter ='r/' + config['filter']['latitude'] + "/" + config['filter']['longitude'] + "/" + config['filter']['range']

################################################################
## Define Functions

def exec_proc(conn,proc,values):
    # Executes SQL Stored Procedures - Doesn't return anything

    connection = conn.raw_connection()

    try:
        cursor = connection.cursor()
        cursor.callproc(proc, values)
        cursor.close()
        connection.commit()
    finally:
        connection.close()

def callback(packet):
    # This function is called whenever a new packet is received

    gooddata = False

    if "weather" in packet:
        # Extract weather data from the packet
        weather_data = packet['weather']

        if len(weather_data) > 0: # Check to see if there is actually weather data in the packet

            values = []

            values.append(packet['from'])

            if "ssid" in packet:
                values.append(packet['ssid'])
            else:
                values.append(0)

            if "temperature" in weather_data:
                values.append(weather_data['temperature'])
            else:
                values.append(0)

            if "pressure" in weather_data:
                values.append(weather_data['pressure'])
            else:
                values.append(0)

            if "wind_gust" in weather_data:
                values.append(weather_data['wind_gust'])
            else:
                values.append(0) 

            if "wind_speed" in weather_data:
                values.append(weather_data['wind_speed'])
            else:
                values.append(0)

            if "wind_direction" in weather_data:
                values.append(weather_data['wind_direction'])
            else:
                values.append(0)

            if "rain_1h" in weather_data:
                values.append(weather_data['rain_1h'])
            else:
                values.append(0)

            if "rain_24h" in weather_data:
                values.append(weather_data['rain_24h'])
            else:
                values.append(0)

            if "rain_since_midnight" in weather_data:
                values.append(weather_data['rain_since_midnight'])
            else:
                values.append(0)

            if "humidity" in weather_data:
                values.append(weather_data['humidity'])
            else:
                values.append(0)

            if "luminosity" in weather_data:
                values.append(weather_data['luminosity'])
            else:
                values.append(0)

            values.append(str(packet).replace("'","''"))
            proc_name = 'insert_wx'
            gooddata = True

    else: # Position Report
       
        values = []

        if "from" in packet:
            values.append(packet['from'].replace("'", ""))
        else:
            values.append('')
        
        if "ssid" in packet:
            values.append(packet['ssid'])
        else:
            values.append(0)
        
        if "latitude" in packet:
            values.append(packet['latitude'])
        else:
            values.append(0)
        
        if "longitude" in packet:
            values.append(packet['longitude'])
        else:
            values.append(0)
        
        if "course" in packet:
            values.append(packet['course'])
        else:
            values.append(0)
        
        if "speed" in packet:
            values.append(packet['speed'])
        else:
            values.append(0)
        
        if "altitude_ft" in packet:
            values.append(packet['altitude_ft'])
        else:
            values.append(0)

        if "comment" in packet:
            values.append(packet['comment'].replace("'", ""))
        else:
            values.append('')

        values.append(str(packet).replace("'","''"))
        proc_name = 'insert_pos'
        gooddata = True
        
    # Execute SQL insert Procedure
    if gooddata:
        exec_proc(db_engine, proc_name, values)

def aprs_connect():
    # Connect to APRS-IS and start Processing

    while True:
        try:
            AIS.connect()
        except aprslib.exceptions.ConnectionError:
            print("Connection to APRS server failed, trying again in 30 seconds...")
            sleep(30)
            continue 
        else:
            print(f"Connected to APRS-IS")
            print(f"Listening for packets on port {port} with filter {set_filter}")
            break

    AIS.consumer(callback, raw=False)
   

    
################################################################
## Main Driver

# Create APRS IS instance
AIS = aprslib.IS(callsign, passwd = passcode, port=port)
AIS.set_filter(set_filter)

# Connect to APRS-IS and start processing
while True:

    try:
        aprs_connect()

    except aprslib.exceptions.ConnectionDrop:
        print("Connection to APRS server dropped, trying again in 30 seconds...")
        sleep(30)
        continue
    except aprslib.exceptions.ConnectionError:
        print("Connection to APRS server failed, trying again in 30 seconds...")
        sleep(30)
        continue 
    except KeyboardInterrupt:
        print("Program interrupted, exiting...")
        break
    except Exception as e:
        print(f"Unexpected error: {e}")
        sleep(30)
        continue
