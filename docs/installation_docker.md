# Docker

This application can be run in Docker and the image built in one of two ways. Running it in Docker is the recommended way to run the application.

The following uses docker compose to bring up the container. If you don't want to use docker compose or are using some other container manager, you will need to configure it yourself. Some of the inststructions below will be useful still though.

All commands are for Linux. If you run Docker a different way, you will need to adjust for that as well.

## Building the Image from Repo

You can build the container image locally if you choose from the repo.

First, clone the repo:

```bash
git clone https://github.com/n8acl/aprstosql.git
```

Next, follow the instructions in the Configuration Guide (See menu to the left) to setup the config file and then come back here.

There is a sample ```docker-compose.yaml``` file in the repository that you can edit. Open the ```docker-compose.yaml``` and find the ```volumes``` section. 

Make sure to set the path to where your config file is located by changing the ```<path to your folder>``` tag.

```yaml
    volumes:
      - /<path to your folder>/aprstosql/config.json:/app/config.json
```
Once the configuration file has been set and the ```docker-compose.yaml``` file has been edited, you can build the image using the following command:

```yaml
docker-compose build
```

After the the image has been built, bring up the container:

Depending on the version of docker compose you are using:

```bash
docker compose up -d
```

**- OR -**

```bash
docker-compose up -d
```

## Using Image from Docker Hub

If you don't want to build the image yourself, the container can be pulled from the Docker Hub. The container is built with multiarch support and can be run on an x86 machine or a Raspberry Pi.

Create a directory to house the needed files:

```bash
mkdir aprstosql
```

Move into the directory:

```bash
cd aprstosql
```

Then, you will need to grab a couple of files from the repo and put them into the directory you just created:

```bash
wget https://github.com/n8acl/aprstosql/blob/main/config.json
wget https://github.com/n8acl/aprstosql/blob/main/docker-compose.yaml
```

Next, follow the Configuration Guide to set the config file and then come back here.

Next, edit the ```docker-compose.yaml``` file and change the following:

- Find the line that says ```build: .```
    - Change this to ```image: n8acl/aprstosql:latest```

```yaml
    build: .
```

- Find the volumes section. 
   - Make sure to set the path to your configuration file by changing the ```<path to your folder>``` tag.
  
```yaml
    volumes:
      - /<path to your folder>/aprstosql/config.json:/app/config.json
```


Save the file.

Now pull the image:

Depending on the version of docker compose you are using:

```bash
docker compose pull
```

**- OR -**

```bash
docker-compose pull
```

Once it is pulled, bring it up:

Depending on the version of docker compose you are using:

```bash
docker compose up -d
```

**- OR -**

```bash
docker-compose up -d
```

## Verify the Data

Once the container is running, you should be able to see a new database called APRS in SQL Server along with the tables and procedures needed. To verify that data is flowing in to the database, open either SQL Server Management Studio or Azure Data Studio and run the following commands in a new query.

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

Once the database has been created, you can stop the container and bring it back up at will as needed. If you drop the APRS database from SQL Server at any point, when you run the container again, it will recreate the database. 