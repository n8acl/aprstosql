import sqlalchemy as db
from sqlalchemy import func, Computed
from sqlalchemy_utils import database_exists, create_database

import src.db_functions as dbf
import src.db_conn as dbc

def create_db():

    #############################
    # Define Database Engine

    try:
        db_engine = dbc.db_connection()
        print("Database Connection established")
    except Exception as e:
        print("Database Connection could not be established.", e)

    #############################
    # create new Database

    create_database(db_engine.url)

    metadata = db.MetaData()

    print("Creating Tables....")

    pos = db.Table('pos', metadata,
                    db.Column('callsign',db.String(20)),
                    db.Column('ssid',db.Integer()),
                    db.Column('lat',db.Float()),
                    db.Column('lon',db.Float()),
                    db.Column('course',db.Integer()),
                    db.Column('speed',db.Integer()),
                    db.Column('altitude_ft',db.Integer()),
                    db.Column('comment',db.String(5000)),
                    db.Column('raw_data',db.String(8000)),                    
                    db.Column('time_in',db.DateTime(timezone=True), server_default=func.now())
    )

    wx = db.Table('wx', metadata,
                    db.Column('callsign',db.String(20)),
                    db.Column('ssid',db.Integer()),
                    db.Column('tempC',db.Float()),
                    db.Column('tempF',db.Float(), Computed('9.0/5.0 * tempC + 32')),
                    db.Column('pressure',db.Float()),
                    db.Column('wind_gust',db.Float()),
                    db.Column('wind_speed',db.Float()),
                    db.Column('wind_direction',db.Float()),
                    db.Column('rain_1h',db.Float()),
                    db.Column('rain_24h',db.Float()),
                    db.Column('rain_since_midnight',db.Float()),
                    db.Column('humidity',db.Float()),
                    db.Column('luminosity',db.Float()),
                    db.Column('raw_data',db.String(8000)),                    
                    db.Column('time_in',db.DateTime(timezone=True), server_default=func.now())
    ) 

    metadata.create_all(db_engine)