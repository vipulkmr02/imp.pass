### IMP.PASS developer's guide


## What is IMP.PASS

Imp.pass is a simple password manager. It currently only saves your passwords &
using the interpreter one can retrieve his/her passwords and can save their
passwords.


## Goals

- A server for it, like a web server that sends and receives requests.
- Users should be able to change their master passwords.
- Users should be able to export their passwords.
- A Web based UI
- A Qt based UI


## How to use

To use IMP.PASS, you will need a MySQL databse to store the data, You will have
to install a MySQL server and also modify the `src/settings.json` according to
your server's address. Change the `databaseHost` to your server's host and
`databasePort` to your server's port `databaseUser` and `databasePassword` to
your server's credentials. After configuring the `settings.json` 

If you're unable to setup the database server. You can use Docker to create a
MySQL database server. Docker is what I use to manage my MySQL server on my
machine, reason is, **It does not interfere with my OS's softwares and
dependencies**. Using the given scripts, setting up a MySQL database server is a breeze.


# How to Use Scripts:

- `db-script.sh`: Creates a Docker container of MySQL database server if you
  don't have the MySQL server docker image, don't worry Docker will pull it out
  for you :). Notice that you can change the password of the database sever by
  editing the script.

- `reset.sh`: Creates all the schemas in the database. If your database gets
  messed up, you can reset your schemas with this script. This script will show
  you an error message if you just ran it after running the `db-script.sh`
  because it takes some time to setup the docker database. Generally it will
  not take more tha 3-4 tries to reach the database, but if running the script
  2nd time also gives the same error message then you should check the docker
  container of the database server. If it's not running (`docker ps`). Brew it
  up again using the `db-script.sh`.

- activate.sh: Activates the python virtual environment. If you're on
  Windows. you need to create your own virtual environment and make sure to
  install those requirements using the following command:
  `python3 -m pip install -r requirements.txt`
  **OR**
  `pip install -r requirements.txt`.

**WARNING: The virtual environment(ip) here is according to a Linux environment**

## Running the project
- STEP-1: run `db-script.sh`
- STEP-2: run `reset.sh`
- STEP-3: activate `virtual environment`
- STEP-4: run the interpreter script in the src directory
