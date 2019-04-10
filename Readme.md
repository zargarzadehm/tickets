# **Ticket Project** [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://gitlab.com/zargarzadehm/tickets)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![Build](https://img.shields.io/bitbucket/pipelines/atlassian/adf-builder-javascript/task/SECO-2168.svg)
![PyPI - Status](https://img.shields.io/pypi/status/Django.svg)
![Read the Docs](https://img.shields.io/readthedocs/pip.svg)

This is Ticket Management system using Tornado Web server.

stable release version: ![version](https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000)

Author : Moein Zargarzadeh

Language : Python 3.6.5




# **PreRequirements**

For This Project You Need below Requirements :
* python
* mysql
    * For install MySql I suggest to you install docker <a href="https://docs.docker.com/install/" target="_blank">**here**</a> and run this command :
```shell
$ docker run -d -p 3306:3306 --name=mysql-server --env="MYSQL_ROOT_PASSWORD=Your password" mysql
```
Otherwise run this command for install python and mysql:

```shell
$ apt install python mysql
```

# **Requirement**

For runnig this project You Need to run below command for install dependensi  :

```shell
$ pip install -r requirements.txt
```

# **install**
## Step0 : Cloning

First of All Clone the Project : 

```shell
$ https://gitlab.com/zargarzadehm/tickets.git
```

## Step1 : Connect to MySQL and create a database

Connect to MySQL as a user that can create databases and users:

```shell
$ mysql -u root
```
    
Create a database named "tickets":
    
```shell
mysql> CREATE DATABASE tickets;
```
    
Allow the "admin" user to connect with the password "12345689":
    
```shell
mysql> CREATE USER PRIVILEGES tickets.* 'admin'@'localhost' IDENTIFIED BY '12345689';
mysql> GRANT ALL PRIVILEGES ON tickets.* TO 'admin'@'%';
mysql> FLUSH PRIVILEGES;
```

## Step2 : Create the tables in your new database

You can use the provided ticketdb.sql file by running this command:

```shell
$ mysql --user=admin --password=12345689 --database=tickets < ticketdb.sql
```

You can run the above command again later if you want to delete the
contents of the tickets and start over after testing.

Then now you Must Put Database information in code.py from line 13 - 16

## Step3 : Run the ticket project server


With the default user, password, and database go to directory server and you can run:

```shell
$ cd server
$ python sever.py
```

If you've changed anything, you can alter the default MySQL settings
with arguments on the command line, e.g.:

```shell
$ python sever.py --mysql_user=moein --mysql_password=zargarzadeh --mysql_database=tickets
```

# **Usage**

Now For Sending Requests You Have 2 Options :
1. Postman
2. Our Client Code

## POSTMAN :
Download and install <a href="https://www.getpostman.com/apps" target="_blank">**Postman**</a>. 

In our Project We Support POST & GET Method for special Requesting

### You Can See Example Below : 

![Sample Video](http://neolyze.com/wp-content/uploads/2019/ticket-project-Server.mov)

## OUR CLIENT CODE:

Just Go To Client Folders and Run Below Code : 

```shell 
$ python3 client.py
```

![Sample Video](http://neolyze.com/wp-content/uploads/2019/ticket-project-client.MOV)

# **Support**

Reach out to me at one of the following places!

- Telegram at <a href="https://t.me/zargarzadehmoein" target="_blank">@zargarzadehmoein</a>
- Gmail at <a href="mailto:moein@neolyze.com" target="_blank">moein@neolyze.com</a>

# **License**

[![License](https://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
- Copyright 2018 © <a href="https://gitlab.com/zargarzadehm/tickets" target="_blank">ticket Project</a>.

