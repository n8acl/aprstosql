# Database Description

This is a list of all the objects that are created by the script in your database for reference.

- Database Name: APRS

Tables:

pos - This holds the postion data from the stream

```sql
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
```

wx - This holds the weather data from the stream

```sql
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
```

Procedures:

- insert_pos
    - inserts the position data sent from the script
- insert_wx
    - inserts the weather data sent from the script