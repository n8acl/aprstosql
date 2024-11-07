## Description

APRStoSQL is a python script designed to stream APRS data into an Database Server.

Database Servers Supported:
- SQL Server
- MySQL/MariaDB

The Script will connect to the APRS-IS backbone, filter the data coming in and stream it to a database for any other uses. 

There is no processing on the data other then parsing it from the APRS-IS data stream.

This script can be run either as a standalone application or in Docker.

### Features
- Connects to the APRS-IS
- Filters the data from the backbone
- Streams the data to a Database Server

### Use Cases

- Get a small historical track of stations using APRS
- Get a more "Realtime" feel for the weather in your area

## History

This script was born out of the want to have something I had years ago. Back in the day (2006 or so) I was using UI-Vew32 as my APRS Client in my office at home. It had a plug-in that would allow me to redirect the data from the client to a SQL Server Database. I was then able to use that data to look at weather conditions around the area or to get a track history for my friends.

UI-Vew32 stopped being developed, even though there are some who still use it, but I have since moved on to other clients. But for a long time I wanted a way to have that functionality of sending the data to a database again. So I decided it was time to sit down and recreate the functionality as a stand-alone project. Thus APRStoSQL was born.

This script does use MS SQL Server as a database system. While this is not an open source RDBMS like MySQL/MariaDB and others, it is something that is available for use as a free RDBMS with the developer edition and can be run on either Windows or Linux or in Docker. AS long as you are not using SQL Server in a production environment or way, the delveoper edition is free. I use SQL Server for work and like to be up on current technologies, so I have it running here in my home lab for other things.

However, MySQL/MariaDB support is also available in the script.
