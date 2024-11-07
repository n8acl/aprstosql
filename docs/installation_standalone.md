# Standalone Application

When running this as a standalone application (Meaning you are running from the command line with Python directly) you will need to take some steps to make sure things are installed.

## Cloning the repo 

First you will need to clone the repo, please run the following command:

```bash
git clone https://github.com/n8acl/aprstosql.git
```

## Installing Dependencies

Next you will need to make sure that the needed software and python libraries are installed. Please run the following commands to make sure:

```bash
sudo apt-get install -y python3 python3-pip screen

cd aprstosql

pip3 install -r requirements.txt --break-system-packages
```

## Setting Configuration File

Once you have the repo cloned and the software/python libraries installed, you will need to set the configuration file.

Please see the Configuration File documentation for more information and then come back here. (See menu to the left side for the link)

## Running the Script

Once the config file is setup, you can now run the script. To do so, run the following commands, first making sure that you are in the aprstosql directory:

```bash
cd aprstosql

screen -R aprstosql

python3 aprstosql.py
```

## Verify the Data

Once the script is running, you should be able to see a new database called APRS in SQL Server along with the tables and procedures needed. To verify that data is flowing in to the database, open either SQL Server Management Studio or Azure Data Studio and run the following commands in a new query.

```sql
use APRS
go

select 
    *
from pos
order by time_in desc

select
    *
from wx
order by time_in desc
```

These should return result grids with the data in the tables and when you re-execute the queries you should see the data update over time.

Once the database has been created, you can stop the container and bring it back up at will as needed. If you drop the APRS database from SQL Server at any point, when you run the script again, it will recreate the database. 

You should be good to go. Close out of screen to leave the script running:

```Ctrl-A-D```

If there is an error or you need to restart the script for some reason, you can reconnect to the screen session by using:

```bash
screen -R aprstosql
```