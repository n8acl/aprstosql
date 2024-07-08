# Managing the APRS Data

This project was not created with the intent to create a backup of all APRS data over time. Even though we are filtering the APRS data from the stream, this still loads a ton of data over said period of time. You will need to manage the data otherwise the database will bloat and become huge. 

Using the queries below, you can create a stored procedure or job in SQL Server that will delete the data based on a time frame.

```sql
------------------------------------------
-- Clean up APRS Database tables
-- Deletes data 2 weeks old from today

delete from aprs.dbo.pos
where time_in <= dateadd(d, -14, getdate())

delete from aprs.dbo.wx
where time_in <= dateadd(d, -14, getdate())
```

These queries delete any data that is 2 weeks old from today from my database. Anything over that is too stale for me to use. This helps keep the database managable. Your mileage my vary though and you might want a longer time frame for farther analysis of the data if needed.

I have these in a stored procedure with other data table cleanup functions and have a job setup to run my data cleanup daily. 