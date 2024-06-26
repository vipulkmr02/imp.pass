## What is IMP.PASS

Imp.pass is a simple password manager. It currently only saves your passwords by
encrypting them based on your master password. It's interfaces are under
progress. It can also be used as a private password vault on a private network.


## How to setup

To use IMP.PASS, you will need a MySQL databse to store the data, You will have
to install a MySQL server and also modify the `src/settings.json` according to
your server's address. Change the `databaseHost` to your server's host and
`databasePort` to your server's port `databaseUser` and `databasePassword` to
your server's credentials. After configuring the `settings.json` 

If you're unable to setup the database server. You can use Docker to create a
MySQL container. Docker is what I used to develop this project on my machine
MySQL server on my machine, reason is, **It does not interfere with my OS's
softwares and dependencies**. Using the given scripts, setting up a MySQL
server container is a breeze.


## How to Use Scripts:

- `mysql-container`: Creates a Docker container of MySQL database server if you
  don't have the MySQL server docker image, don't worry Docker will pull it out
  for you. Notice that you can change the password of the database sever by
  editing the script.

- `db-reset`: Creates all the schemas in the database. If your database gets
  messed up, you can reset your schemas with this script. This script will show
  you an error message if you just ran it after running the `mysql-container.sh`
  because it takes some time to setup the docker database. Generally it will
  not take more tha 3-4 tries to reach the database, but if running the script
  2nd time also gives the same error message then you should check the docker
  container of the database server using `docker ps`.


## Running the Interpreter (CLI)

- STEP-0: Create a Virutal Environment by `python3 -m venv venv`.
- STEP-1: Install all required python packages by `pip install -r requirements.txt`.
- STEP-2: Run `mysql-container.sh` to setup MySQL container (SKIP if having a DB already).
- STEP-3: Run `db-reset.sh` to create Schemas.
- STEP-4: go to the `src` directory and run interpreter.py.


## Goals

- A socket-based-server for it, like a web server that sends and receives requests.
- Users should be able to change their master passwords.
- Users should be able to export their passwords.
- A Web based UI
- A Qt based UI