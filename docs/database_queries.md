# Helpful Queries

Here are some example queries that you can use to query the data from the database when needed.

These are written for SQL Server, so if you use MySQL, you will have to modify them to work properly.

These are all the queries talked about through out this Wiki all in one place.

## View the data

Mentioned in the Standalone/Docker documents.

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

## Clean up the Data 

Mentioned in the Data Management documents.

```sql
------------------------------------------
-- Clean up APRS Database tables
-- Deletes data 2 weeks old from today

delete from aprs.dbo.pos
where time_in <= dateadd(d, -14, getdate())

delete from aprs.dbo.wx
where time_in <= dateadd(d, -14, getdate())
```