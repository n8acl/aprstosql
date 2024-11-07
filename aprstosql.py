#!/usr/bin/env python3

import json
import aprslib
import pymssql # SQL Server
import pymysql # MySQL
import sqlalchemy
from sqlalchemy import text as sqltext, select, MetaData, Table
from sqlalchemy_utils import database_exists, create_database
from time import sleep

import src.db_functions as dbf
import src.db_conn as dbc
import src.db_create as cdb


#############################
# import config json file

with open("config.json", "r") as read_file:
    config = json.load(read_file)


############################################################################
##  SQL Server Connection creation

# define SQL Server connection variables
sql_host = config['database']['credentials']['host']
sql_user = config['database']['credentials']['username']
sql_password = config['database']['credentials']['password']
sql_database = 'APRS'

# configure SQL Server Database connection with SQL Alchemy

try:
    db_engine = dbc.db_connection()
    print("Database Connection established")
except Exception as e:
    print("Database Connection could not be established.", e)

if not database_exists(db_engine.url):
    print("Error Connecting to Database. Does not exist. Creating database....")
    cdb.create_db()

metadata = sqlalchemy.MetaData()
metadata.reflect(bind=db_engine)

pos = metadata.tables['pos']
wx = metadata.tables['wx']

################################################################
## Define Variables
linefeed = "\n"
callsign = config['callsign']
port = 14580
passcode = aprslib.passcode(callsign)
# set_filter ='r/39.1/-84.6/100'
set_filter ='r/' + config['filter']['latitude'] + "/" + config['filter']['longitude'] + "/" + config['filter']['range']

################################################################
## Define Functions

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
            table_name = 'wx'
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
        table_name = 'pos'
        gooddata = True
        
    # Execute SQL inserts
    if gooddata:
        values_list = []
        if table_name == 'wx':
            sql = wx.insert()
            values_list= [{'callsign':values[0],
                            'ssid': values[1],
                            'tempC': values[2],
                            'pressure': values[3],
                            'wind_gust': values[4],
                            'wind_speed': values[5],
                            'wind_dir': values[6],
                            'rain_1h': values[7],
                            'rain_24h': values[8],
                            'rain_midnight': values[9],
                            'humidity': values[10],
                            'luminosity': values[11],
                            'raw_data': values[12]
            
            }]
        else:
            sql = pos.insert()
            values_list= [{'callsign':values[0],
                            'ssid': values[1],
                            'latitude': values[2],
                            'longitude': values[3],
                            'course': values[4],
                           'speed': values[5],
                            'altitude_ft': values[6],
                            'comment': values[7],
                            'raw_data': values[8]
            
            }]

        dbf.insert_sql(db_engine, sql, values_list)

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
