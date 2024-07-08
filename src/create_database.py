from sqlalchemy import text as sqltext

def exec_sql(conn,sql):
    # Executes SQL for Updates, inserts and deletes - Doesn't return anything
    conn.execute(sqltext(sql))

def create_db(conn):

    sql = """
            use APRS
        """

    exec_sql(conn, sql)

    sql = """
            drop table if exists pos
        """

    exec_sql(conn, sql)

    sql = """
            create table pos(
                pos_id int identity(1,1) primary key not null, 
                callsign varchar(20) null,
                ssid int null,
                lat decimal(18,2) null,
                lon decimal (18,2) null,
                course int default(0),
                speed int default(0),
                altitude_ft int default(0),
                comment varchar(max) null,
                raw_data varchar(max) null,
                time_in datetime2 default(getdate())

            )

         """

    exec_sql(conn, sql)

    sql = """

            drop table if exists wx

        """

    exec_sql(conn, sql)

    sql = """
            create table wx(
                wx_id int identity(1,1) primary key not null,
                callsign varchar(20) null,
                ssid int null,
                tempC float null,
                tempf as 9.0/5.0 * tempC + 32,
                pressure float null,
                wind_gust float null,
                wind_speed float null,
                wind_direction float null,
                rain_1h float null,
                rain_24h float null,
                rain_since_midnight float null,
                humidity float null,
                luminosity float null,
                raw_data varchar(max),
                time_in datetime2 default(getdate())
            )


        """

    exec_sql(conn, sql)

    sql = """

            drop procedure if exists insert_pos
        """

    exec_sql(conn, sql)

    sql = """
            create procedure insert_pos 
                @callsign varchar(20),
                @ssid int,
                @lat decimal(18,2),
                @lon decimal (18,2),
                @course int,
                @speed int,
                @altitude_ft int,
                @comment varchar(max),
                @raw_data varchar(max)

            as
            begin
                SET QUOTED_IDENTIFIER OFF;
                insert into pos(callsign, ssid, lat, lon, course, speed, altitude_ft, comment, raw_data)
                values(@callsign, @ssid, @lat, @lon, @course, @speed, @altitude_ft, @comment, @raw_data)
                SET QUOTED_IDENTIFIER ON;	

            end


        """

    exec_sql(conn,sql)

    sql = """
            drop procedure if exists insert_wx
        """

    exec_sql(conn, sql)

    sql = """
            create procedure insert_wx 
                @callsign varchar(20),
                @ssid int,
                @tempC decimal(18,2),
                @pressure decimal(18,2),
                @wind_gust decimal(18,2),
                @wind_speed decimal(18,2),
                @wind_direction decimal(18,2),
                @rain_1h decimal(18,2),
                @rain_24h decimal(18,2),
                @rain_since_midnight decimal(18,2),
                @humidity decimal(18,2),
                @luminosity decimal(18,2),
                @raw_data varchar(max)

            as
            begin
                SET QUOTED_IDENTIFIER OFF;
                insert into wx(callsign, ssid, tempC, pressure, wind_gust, wind_speed, wind_direction, rain_1h, rain_24h, rain_since_midnight, humidity, luminosity, raw_data)
                values(@callsign, @ssid, @tempC, @pressure, @wind_gust, @wind_speed, @wind_direction, @rain_1h, @rain_24h, @rain_since_midnight, @humidity,	@luminosity, @raw_data)
                SET QUOTED_IDENTIFIER ON;

            end

        """

    exec_sql(conn,sql)

    conn.close()