# Configuration Guide

This script uses a JSON file to load the configuration information into the script.

You will need the ```config.json``` from the repo for the script to work properly.

However you run the script (standalone or in Docker) this file will need to be loaded with the correct settings. All Settings are ***required***.

Edit the ```config.json``` in your editor of choice. It should look something like this:

```json
{

    "callsign": "<YOUR CALLSIGN HERE>",
    "filter" :{
        "latitude": "<YOUR LATITUDE HERE FORMAT XX.X>",
        "longitude": "<YOUR LONGITUDE HERE FORMAT XX.X>",
        "range": "<RANGE IN MILES ex: 100>"
    },

    "database": {
    "rdbms_type": "mssql",
    "credentials": {
      "username": "<SQL SERVER USERNAME HERE>",
      "password": "<SQL SERVER PASSWORD HERE>",
      "host": "<SQL SERVER HOST HERE>"
    }

}
```

- Callsign: This is your Callsign. Enter it here, replacing ```<YOUR CALLSIGN HERE>```.
- Filter: This is how we are going to set the filter for the APRS Stream
    - Latitude: this is your latitude in XX.X format. Ex: 84.1. Replace ```<YOUR LATITUDE HERE FORMAT XX.X>```
    - Longitiude: Same as latitude, but only your longitude instead. Ex: -84.1. Replace ```<YOUR LONGITUDE HERE FORMAT XX.X>```
    - Range: This is the range in Miles you want to filter the data from the coordinates you set above. ***NOTE***: There is not an option for all data coming in because that would be way to much data to handle. Replace ```<RANGE IN MILES ex: 100>```
- database: This is connection info for your Database Server instance. 
    - ***NOTE***: It is not recommended you use a System Administrator account for access. Setup a user that has the ability to at least create databases, tables and has the ability to insert data into tables. 
    - rdbms_type: This is the type of database you are using. Options are:
        - mssql - SQL Server
        - mysql - MySQL/MariaDB Server
    - credentials: This is where you set the connection credentials
        - host: This is the host information for your SQL Server instance. This can be an IP Address or FQDN. Ex's: 10.0.0.25 or mydatabase.local Replace ```<SQL SERVER HOST HERE>```
        - username: This is the username the script will use to connect to your database instance. Ex: myuser. Replace ```<SQL SERVER USERNAME HERE>```
        - password: This is the password for the username above to connect to your database instance. Ex: mypassword. Replace ```<SQL SERVER PASSWORD HERE>```

Once the information has been entered, save the file and close your editor.