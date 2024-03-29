# file: zero.py

# author: Vipul Kumar (vipulkmr02@gmail.com)
# Date created: 10 Feb, 2024
# Description: This file is the first file meant to be run on your system It's
# named zero, cause I wanted it to be a setup like file. This file aims to
# setup all the dependencies and requirements to setup the project

import commons
from time import sleep
import platform
# from os import system
import db


def connect(DB):
    try:
        DB.connect(
            commons.settings["databaseUser"],
            commons.settings["databasePassword"]
        )

    except db.mysql.errors.OperationalError:
        print("Unable to connect with the Database")
        for i in range(3):
            print(f"Retrying in {3-i}\r", end='')
            sleep(1)
        connect(DB)


SYSTEM_TYPE = platform.system()

commons.echoAndLog(f"{SYSTEM_TYPE} system detected", 20)

# Schemas creation
with open('sql-setup.sql') as sqlFile:
    SQL_TO_EXECUTE = sqlFile.read().replace('\'%\'', commons.host)

DB = db.Database()
connect(DB)
DB.cursor.execute(SQL_TO_EXECUTE, multi=True)
commons.echoAndLog("Database setup successful", 20)
exit(0)
