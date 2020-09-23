iMessage SMS database browsing web app
======================================
This is a fork of jsok's repo [here](https://github.com/jsok/django-imessage). I have refactored some of the code, added functionalities and will continue to added functionalities to it as it seems to be a useful tool that elegantly solves a widely researched and discussed topic, how to read and search Apple's iMessages.

The readme below is a modified version of jsok's to reflect the changes I've made.

What?
-----
iOS and OSX store all your iMessages/SMS texts in a sqlite database. This gets downloaded to your computer each time you backup/sync your phone via iTunes.

This is a django app which allows you to drop your iMessage/SMS database(s) into it, fire it up and have all your messages and databases in a nice browseable web app. In addition to just viewing your messages, you can also filter by date and/or query search terms.

Why?
----
Why not? iOS and OSX will only show the most recent 100 or so messages on the screen, to view older ones you need to hit "Load Earlier Messages" and wait. Too bad if you want to see messages from last month, or even last year! With this app you can see them all, go to a specific date for a conversation and/or search them.

How?
----
The iMessage/SMS database has been analysed by many and its schema is well known. I've taken some of this info and used it to convince django's ORM into reading it.

**For iOS:**

If you have a jailbroken device:

* SSH into your device
* Navigate to `/var/mobile/Library/SMS/`
* scp sms.db to your computer

If you do not have a jailbroken device or you do not want to use ssh:

* Backup your iphone locally on your computer
* Navigate to `~/Library/Application Support/Mobile Sync/Backup/<device id>/3d0d7e5fb2ce288813306e4d4636395e047a3d28`
* Copy the db file somewhere

**For OSX**

* Open terminal.app
* Navigate to `~/Library/Messages/`
* Copy chat.db somewhere

As of OSX 10.15 and with iCloud message sync on it seems like users cannot access the `~/Library/Messages/` directory (I cannot confirm when or what caused this) so do the following steps instead:

1. Open terminal.app
2. `open ~/Library/Messages/`
3. Copy `chat.db` to the cloned github directory

Screenshot
----------
![Screenshot](https://raw.github.com/clayshieh/django-imessage/master/messages_screenshot.png)

Setup
-----
Requirements are:
 - django 1.4
 - pytz

1. edit `core/settings.py` and set your TIME_ZONE (list of timezones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones))
2. Then drop your iMessage/SMS database(s) in `sms/db/`
3. run `python manage.py runserver`
4. Navigate to `http://localhost:8000/databases/` and select the database you wish to view

Navigate to `http://localhost:8000` for instructions in general

Docker Setup
------------
1. [Install Docker](https://docs.docker.com/get-docker/)
2. Run the container with the following command:
`docker run -it -p 8000:8000 -v <path to chat.db or sms.db>:/sms/db/sms.db clayshieh/django-imessage:latest`
3. Navigate to `http://localhost:8000`

Updates
-------
9/22/2020

 - Dockerized the app and updated instructions for OSX
 - I have not worked on or updated this app in quite a while. There have been a lot of changes in both iOS and OSX so if you have any issues while using the app please let me know
 - I did not realize that issues cannot be opened on forked repos, I will be moving all the code to a new repo and leaving this repo as a pointer once I either get permission from [jsok](https://github.com/jsok) and refactor the code

Future TODO
-----------
 - ~~Messages.app style timestamps (supressed timestamps when messages are received within a given time delta)~~
 - ~~Some way of searching your messages~~
 - Update to Django 1.11
 - Add support attachments if it is a OSX database
 - Add contact import support to associate numbers with canonical names
 - Add support for group chats
 - Convert message data to REST endpoints so UI doesn't hang when loading
 - Make setup process user friendly in terms of uploading user db, uploading attachments directory, etc.
 - ~~Support multiple database selection~~
 - ~~Add exporting functionality~~
