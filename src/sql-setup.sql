-- sql-setup.sql
-- This file has the SQL code which can get the IMP.PASS started
-- IMP.PASS requires some tables and DATABASES to already setup before doing anything

-- Creating databases
CREATE DATABASE IF NOT EXISTS ip;
CREATE DATABASE IF NOT EXISTS weirddb;
CREATE DATABASE IF NOT EXISTS kamandb;

-- Creating users
CREATE USER  IF NOT EXISTS ip@'%' IDENTIFIED BY 'hello123';
GRANT CREATE USER, DROP ON *.* TO ip@'%';
GRANT CREATE, ALTER, UPDATE ON *.* TO ip@'%' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON ip.* TO ip@'%';

-- Granting permissions
CREATE USER  IF NOT EXISTS weird@'%' IDENTIFIED BY '#@$#3$';
CREATE USER  IF NOT EXISTS namk@'%' IDENTIFIED BY 'iwantlesssalt';
GRANT ALL PRIVILEGES ON weirddb.* TO weird@'%';
GRANT ALL PRIVILEGES ON kamandb.* TO namk@'%';

-- Creating Tables
CREATE TABLE ip.users ( 
	username VARCHAR(20) UNIQUE NOT NULL PRIMARY KEY,
	created_on DATETIME NOT NULL
);

CREATE TABLE weirddb.a ( 
	username VARCHAR(20),
	weird VARBINARY(1024) NOT NULL,
	FOREIGN KEY (username) REFERENCES ip.users(username)
);

CREATE TABLE kamandb.a ( 
	username VARCHAR(20) ,
	namk VARBINARY(1024) NOT NULL,
	FOREIGN KEY (username) REFERENCES ip.users(username)
);
