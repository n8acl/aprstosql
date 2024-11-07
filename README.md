# APRStoSQL

###### Current Release 07032024

APRStoSQL is a python script designed to stream APRS data into a Database Server.

The Script will connect to the APRS-IS backbone, filter the data coming in and stream it to a Database for any other uses.

This script was born out of the want to have something I had years ago. Back in the day (2006 or so) I was using UI-View32 as my APRS Client in my office at home. It had a plug-in that would allow me to redirect the data from the client to a SQL Server Database. I was then able to use that data to look at weather conditions around the area or to get a track history for my friends.

UI-View32 stopped being developed, even though there are some who still use it, but I have moved on to other clients. But for a long time I wanted a way to have that functionality of sending the data to a database again. So I decided it was time to sit down and recreate the functionality as a stand-alone project. Thus APRStoSQL was born.

This script does use MS SQL Server as a database system. While this is not an open source RDBMS like MySQL/MariaDB and others, it is something that is available for use as a free RDBMS with the developer edition and can be run on either Windows or Linux or in Docker. AS long as you are not using SQL Server in a production environment or way, the delveoper edition is free. I use SQL Server for work and like to be up on current technologies, so I have it running here in my home lab for other things.

However, MySQL/MariaDB support is also available in the script.

There is no processing on the data other then parsing it from the APRS-IS data stream.

This script can be run either as a standalone application or in Docker.

This software is intended for use by Amateur Radio Operators only.

Please see [the Wiki](https://n8acl.github.io/aprstosql) for more information on installation and configuration steps as well as running the script.

## Use Cases

- Get a small historical track of stations using APRS
- Get a more "Realtime" feel for the weather in your area

---

## Contact

If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Discord: Ravendos
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

Or open an issue on Github. I will respond to it, and of course you, when I can. Remember, this is a hobby and there are other daily distractors that come first, like work, school and family.

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log

Changes Prior to current year have been moved to the [ChangeLog](https://n8acl.github.io/aprstosql/changelog/) on the wiki.

- 08/27/2024

  - Update README.md for typos
  - Update Wiki for pulling from Docker Hub

- 07/03/2024: Initial Release
