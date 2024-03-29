#!/usr/bin/python3

import os
from commandHandler import CommandHandler
import messify
from sys import argv

query = ""
username, user_cred_file = "", None
TO_BE_LOGOUT = False
TO_BE_CACHED = False
TO_BE_SIGNED_UP = False


class CredFile:
    def __init__(self):
        global username
        self.file_name = f"CredFile_{username}"
        try:
            open(f"../{self.file_name}", "x")
        except FileExistsError:
            pass

    def write(self, content):
        fp = open(f"../{self.file_name}", "w")
        fp.write(messify(content))
        fp.close()

    def append(self, content):
        prev_content = self.read()
        self.write(prev_content + content)

    def read(self):
        return messify.fDemessify(open(f"../{self.file_name}"))

    def destroy(self):
        os.remove(f"../{self.file_name}")


# getting user credentials from arguments
argv = argv[1:]

for arg in argv:
    if "-u" in arg:
        username = arg[2:]
        user_cred_file = CredFile()

    elif "-p" in arg and not TO_BE_LOGOUT and user_cred_file is not None:
        user_cred_file.write(arg[2:])

    elif arg == "--logout" or TO_BE_LOGOUT:
        TO_BE_LOGOUT = True

        if username == "":
            continue
        else:
            user_cred_file.destroy()

    elif arg == "--signup" or TO_BE_SIGNED_UP:
        TO_BE_SIGNED_UP = True

        if username and user_cred_file.read():
            break

    elif arg == "--cache" or TO_BE_CACHED:
        TO_BE_CACHED = True

        if username and user_cred_file.read():
            exit()

        continue

    elif arg == "-q":
        query = argv[argv.index(arg) + 1]


cmdhndlr = CommandHandler()

if TO_BE_SIGNED_UP:
    cmdhndlr.signup(username, user_cred_file.read())
    exit()

if cmdhndlr.login(username, user_cred_file.read()):
    cmdhndlr.query = tuple(query.split())
    cmdhndlr.process_query()
    print(cmdhndlr.output)

else:
    print("LOGIN FAILED")
