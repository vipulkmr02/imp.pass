import json
import logging
# import simple_term_menu
import messify
# from subprocess import Popen, run
# from tempfile import TemporaryFile
from sys import exc_info
import socket

settings = json.load(open("settings.json"))

selected_host = settings["databaseHost"]

if settings['docker-db'] is False:
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect((settings['databaseHost'], settings['databasePort']))
    host = ip.getsockname()[0]
    ip.close()

else:
    host = '172.17.0.1'

logDir = settings["logDir"]

ERROR_MSG = "ERROR ENCOUNTERED!\n" \
            "check logs for further details"

ENCODING_FORMAT = "utf-8"


def traceback(trace):
    logger.error("ERROR occurred")
    with open(f"{logDir}/traceback.txt", "a+") as t:
        t.write(str(trace) + "\n")


logging.basicConfig(
    level=10,
    filename=f"{logDir}/logs.txt",
    filemode="w+")

logger = logging.getLogger()

HELP = "there are 4 commands which are:\n" \
       "\tset, get, delete, update \n\n" \
       "\tset: parameters : <pid> <password>\n\t\tsaves the password with a password identifier\n" \
       "\tget: \n\t\tgets the password using the password identifier\n" \
       "\tdelete: \n\t\tdeletes the password\n" \
       "\tupdate: \n\t\tupdates the password\n"

HELP_header = "IMP-PASS-3\n"
CMD_help = "IMP-PASS\n"\
           "usage: python3 imp-pass.py command [options]\n"\
           ""


def echoAndLog(message: str, level: int):
    if level not in (10, 20, 30, 40, 50):
        logger.debug("func echoAndLog wrong level")
        return -1

    levels = (
        logger.debug,
        logger.info,
        logger.warn,
        logger.error,
        logger.critical
    )
    levels[level//10 - 1](message)
    print(f"{level}: {message}")


def readMess(fname: str) -> dict:
    """
    Returns the demessifed contents of a messified file

    :param fname: file name
    """

    logger.debug("file commons.py function readMess called")
    logger.info(f"Reading messified file {fname}")

    with open(fname) as X:
        ans = messify.fDemessify(X)

    return ans


def messToJson(fname):
    return json.loads(readMess(fname))
