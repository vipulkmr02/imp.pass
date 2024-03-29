import bcrypt
import commons
import db


def authorize(username: str, password: str) -> bool:
    """
    Checks whether the user and password combination is correct or not

    :param username:
    :param password:
    """

    commons.logger.info(f"Authorizing {username}")

    if user_check(username) is False:
        commons.echoAndLog(30, f"{username} does not exists")
        return False

    CREDS = commons.messToJson("creds")
    DATA = commons.messToJson("data")

    # salt
    SALT_UNAME = CREDS["salt"]["username"]
    SALT_PASSWORD = CREDS["salt"]["password"]
    datab = db.Database(DATA["databases"]["salt"])
    datab.connect(SALT_UNAME, SALT_PASSWORD)
    datab.read("namk", table='a', username=username)
    output = datab.fetchone()

    if output is None:
        commons.logger.info(f"{username} is not in database")
        return (False, None)
    else:
        commons.logger.info(f"{username} exists")
        salt = output[0]

    salt = bytes(output[0])
    # got the salt

    datab = db.Database(DATA["databases"]["hash"])

    HASH_UNAME = CREDS["hash"]["username"]
    HASH_PASSWORD = CREDS["hash"]["password"]
    datab.connect(HASH_UNAME, HASH_PASSWORD)

    # print(password, salt)
    # generating the hashed version of the password
    generated_hash = bcrypt.hashpw(
        password.encode(commons.ENCODING_FORMAT),
        salt
    )

    # getting the hash from database
    datab.read("weird", table="a", username=username)
    output = datab.fetchone()
    db_hash = output[0] if output else None
    # got the hash

    datab.close()

    return generated_hash == db_hash


def sign_up(user: str, password: str):
    """
    Creates a new account

    :param user: The `user` argument takes the username
    :param password: The `password` argument takes the password
    """

    commons.logger.info(f"New USER signing up: {user}")

    CREDS = commons.messToJson("creds")
    DATA = commons.messToJson("data")

    master_db = db.Database(DATA["databases"]["master"])
    master_db.connect(
        user=CREDS["master"]["username"],
        host=commons.settings["databaseHost"],
        passwd=CREDS["master"]["password"],
    )
    from datetime import datetime as dt

    created_on = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    master_db.write(user, created_on, table="users")
    master_db.commit()

    datab = db.Database(DATA["databases"]["salt"])
    password_salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(
        password=password.encode(commons.ENCODING_FORMAT), salt=password_salt)
    datab.connect(
        user=CREDS["salt"]["username"],
        passwd=CREDS["salt"]["password"]
    )
    datab.write(user, str(password_salt)[2:-1], table="a")
    datab.commit()
    datab.close()

    datab = db.Database(DATA["databases"]["hash"])
    datab.connect(
        user=CREDS["hash"]["username"],
        passwd=CREDS["hash"]["password"]
    )

    datab.write(user, str(password_hash)[2:-1], table="a")
    datab.commit()
    datab.close()

    master_db.execute("SHOW TABLES")
    tables = master_db.fetchall()

    master_db.execute(
        f"CREATE TABLE {user}(pid VARCHAR(20), penc VARBINARY(255))"
        if user not in tables
        else f"DELETE FROM {user}"
    )

    master_db.create_user(user=user, host=commons.host, password=password)
    master_db.commit()
    master_db.grant_permissions(
        "SELECT",
        "INSERT",
        "DROP",
        "DELETE",
        "UPDATE",
        user=user,
        sql_obj=f"{DATA['databases']['master']}.{user}",
        host=commons.host,
    )

    master_db.close()


def user_check(username: str) -> bool:
    """
    Checks whether the given user exists in the database or not.

    :param username: The `username` parameter takes the name of the user
    which you want to check, whether that exists or not.
    """

    CREDS = commons.messToJson("creds")
    DATA = commons.messToJson("data")

    master_db = db.Database(DATA["databases"]["master"])
    master_db.connect(CREDS["master"]["username"], CREDS["master"]["password"])
    master_db.read("1", username=username, table="users")

    result = master_db.fetchone()
    return result == ((1,))


def delete_user(username: str) -> int:
    CRED = commons.messToJson("creds")
    DATA = commons.messToJson("data")

    master_db = db.Database(DATA["databases"]["master"])
    master_db.connect(
        user=CRED["master"]["username"], passwd=CRED["master"]["password"]
    )
    # sql = f"DELETE FROM users WHERE username='{username}'"
    master_db.cursor.execute(multi=True)
    master_db.cursor.commit()
    master_db.close()

    with db.Database(DATA["databases"]["hash"]).connect(
        user=CRED["hash"]["username"],
        passwd=CRED["hash"]["password"]
    ) as cur:
        cur.execute(f"delete from a where username='{username}'")

    with db.Database(DATA["databases"]["salt"]).connect(
        user=CRED["salt"]["username"],
        passwd=CRED["salt"]["password"]
    ) as cur:
        cur.execute(f"delete from a where username='{username}'")
