#!/usr/bin/env python3

import commons
import db
import encryption as enc
import accounts as acc
import history


class CommandHandler:

    def __init__(self):
        self.commands = ["set", "get", "delete", "update"]
        self.query = []
        self.output = ""
        self.encrypter: enc.AESCipher = None
        self.database: db.Database = None
        self.cursor = None
        self.logged_in = False
        self.username = ""
        self.history = None

    def login(self, username, password) -> int:
        """
        will log the user into the server
        Login successful: 0
        Wrong credentials: 1
        User does not exists: 2
        Something else is wrong: 3
        """

        commons.logger.info(f"attempting login for {username}")
        login_status = acc.authorize(username, password)

        if login_status:
            commons.logger.info("LOGIN SUCCESSFUL")
            self.output = "LOGIN SUCCESSFUL"
            self.logged_in = True
            self.username = username
            MASTER_DB = commons.messToJson('data')["databases"]["master"]
            self.database = db.Database(MASTER_DB)
            self.database.connect(user=username, passwd=password)
            saltDB = db.Database(
                commons.messToJson("data")["databases"]["salt"]
            )
            CREDS = commons.messToJson('creds')
            salt_username = CREDS['salt']['username']
            salt_password = CREDS['salt']['password']
            saltDB.connect(salt_username, salt_password)
            saltDB.read("namk", table="a", username=self.username)
            salt = saltDB.fetchone()[0]
            saltDB.close()
            self.encrypter = enc.AESCipher(password, salt=salt)
            self.cursor = self.database.cursor
            self.history = history.History(username)
            return 0

        else:
            if acc.user_check(username) is False:
                commons.logger.warning("user does not exist")
                self.output = f"{username} does not exists."
                return 1
            else:
                commons.logger.warning("wrong username and password")
                self.output = "Wrong Password"
                return 2
            return 3

    def signup(self, username, password):
        acc.sign_up(username, password)

    def get_query(self):
        """will input the query from the user"""
        if self.logged_in:
            self.query = input("-> ").split()
        else:
            raise Exception("not logged in")

    def set(self):
        if self.query[0] != "set" and len(self.query) != 3:
            return 1

        # checking if there's not already a saved password with same pid
        pid = self.query[1]
        self.database.read("pid", table=self.username, pid=pid)

        if pid == self.database.fetchone():
            self.output = "Password with label '{pid}' already exists."
            return 2

        password = self.query[2]
        penc = self.encrypter.encrypt(password)
        self.database.write(pid, str(penc)[2:-1], table=self.username)
        self.database.commit()
        return 0

    def get(self):
        if self.query[0] != "get" and len(self.query) != 2:
            return 1

        pid = self.query[1]
        self.database.read('penc', table=self.username, pid=pid)
        penc = self.database.fetchone()
        self.output = self.encrypter.decrypt(penc[0]).decode(
            commons.ENCODING_FORMAT
        ) if penc else f"Password for '{pid}' does not exists"
        return 0

    def delete(self):
        if self.query[0] != "delete" and len(self.query) != 2:
            return 1

        pid = self.query[1]
        query = f"DELETE FROM {self.username} WHERE pid='{pid}'"
        self.database.execute(query)
        self.database.commit()
        self.output = f"Password with label '{pid}' deleted."
        return 0

    def update(self):
        if self.query[0] != "update" and len(self.query) != 3:
            return 1

        pid = self.query[1]
        newPassword = self.query[2]
        penc = self.encrypter.encrypt(newPassword)
        del newPassword
        query = f"UPDATE {self.username} "\
                f"SET penc=\"{str(penc)[2:-1]}\" "\
                f"WHERE pid=\"{pid}\""
        self.database.execute(query)
        self.database.commit()
        self.output = f"Password with label '{pid}' updated."
        return 0

    def reset_pwd(newPassword: str):
        """will change the master password"""
        pass

    def process_query(self):
        """will process the query given by the user"""

        self.history.remember(" ".join(self.query))
        if self.logged_in:
            cmnd = self.query[0]

            if cmnd == self.commands[0]:
                return self.set()

            elif cmnd == self.commands[1]:
                return self.get()

            elif cmnd == self.commands[2]:
                return self.delete()

            elif cmnd == self.commands[3]:
                return self.update()

            else:
                return 0

        else:
            self.output = "Not Logged in."

    def fetch_query(self):
        return self.output

    def quit(self):
        self.logged_in = False
        self.database.close()
        self.database = None
        self.cursor = None
        self.username = None
        self.encrypter = None
        self.history.save()
