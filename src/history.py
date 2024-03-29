#!/usr/bin/python3
import os
from datetime import datetime as dt

DIRECTORY = "./.histories"

# History class stores histories of like "anything"


class History:

    @classmethod
    def delete_history(cls, target, multi=False):
        if multi:
            for x in target:
                os.remove(os.path.join(DIRECTORY, x))
        else:
            os.remove(os.path.join(DIRECTORY, target))

    @classmethod
    def delete_all_history(cls):
        for file in os.listdir(DIRECTORY):
            os.remove(os.path.join(DIRECTORY, file))

    def __init__(self, ID, record_time=False):
        self.ID = ID
        self.size = 1000
        self.fpath = os.path.join(DIRECTORY, ID)
        self.record_time = record_time
        self.cur = 0

        if os.path.isfile(self.fpath):
            with open(self.fpath) as fp:
                self.history = fp.readlines()[1:]

        else:
            with open(self.fpath, "x") as fp:
                fp.write(f'!!! CREATION TIME {dt.now().strftime("%D %T")}')
            self.history = []

    def __getitem__(self, index):
        return None if index < 0 else self.history[-index - 1]

    def __setitem__(self, index, message):
        self.remember(message)

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur == len(self.history):
            raise StopIteration
        self.cur += 1
        return self.history[self.cur - 1]

    def remember(self, message):
        if self.record_time:
            message = dt.now().strftime("%D %T") + f" | {message}"

        self.history.append(message)

    def print_history(self):
        print("\n".join(self.history))

    def save(self):
        with open(self.fpath, "a+") as fp:
            fp.seek(0)
            length = len(fp.readlines()) - 1

            fp.seek(0, 2)
            fp.write("\n" + " \n".join(self.history[length:]))

    def reload(self):
        with open(self.fpath) as fp:
            self.history = fp.readlines[1:]
