import mysql.connector as mysql
import commons


DBTYPE = "MySQL"


class Database:
    """The above code defines a class called Database that provides methods for
    connecting to a database, executing queries, fetching results, and managing
    user permissions.

    :param database_name: The `database_name` parameter is used to specify the
    name of the database that you want to connect to. If you don't provide a
    value for this parameter, the connection will be made without specifying a
    database"""

    def __init__(self, database_name=None):
        self.connection = None
        self.cursor = None

        self.dbname = database_name

    def __enter__(self):
        return self.cursor

    def __exit__(self):
        self.cursor.close()

    def connect(self, user: str, passwd: str,
                host=commons.settings["databaseHost"]):
        """
        Creates a connection with the database
        and initializes the cursor object for the database
        """

        conn_params = {
            "host": host,
            "user": user,
            "passwd": passwd,
            "port": commons.settings["databasePort"],
        }

        if self.dbname is not None:
            conn_params["db"] = self.dbname

        commons.logger.info("Connecting to database")
        self.connection = mysql.connect(**conn_params)
        self.cursor = self.connection.cursor()

    def execute(self, query: str):
        commons.logger.debug(f"query executed'{query}'")

        try:
            self.cursor.execute(query)

        except mysql.Error:
            commons.logger.info(query)
            commons.traceback(commons.exc_info())
            print(commons.ERROR_MSG)

    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except Exception:
            commons.traceback(commons.exc_info())
            print(commons.ERROR_MSG)

    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except Exception:
            commons.traceback(commons.exc_info())
            print(commons.ERROR_MSG)

    def fetchmany(self, n):
        try:
            return self.cursor.fetchmany(n)
        except Exception:
            commons.traceback(commons.exc_info())
            print(commons.ERROR_MSG)

    def close(self):
        self.cursor.close()
        self.connection.close()

    def commit(self):
        """Commit the changes"""
        self.connection.commit()

    def read(self, *cols, table, **where):
        """
        Read from the given table
        """
        if len(cols) == 0:
            sql_query = f"SELECT * FROM {table}"

        elif len(cols) == 1:
            sql_query = f"SELECT {cols[0]} FROM {table}"

        else:
            col = str(cols)[1:-1].replace("'", "")
            sql_query = f"SELECT {col} FROM {table}"

        commons.logger.info(sql_query)

        if where:
            sql_query += " WHERE " + " AND ".join(
                f"{key}='{where[key]}'" for key in where
            )

        self.execute(sql_query)

    def write(self, *values, table, where=None):
        if len(values) == 0:
            commons.logger.warn(
                "Attempted to INSERT without specifying values"
            )
            return -1

        if where is None:
            self.execute(f"INSERT INTO {table} VALUES ({str(values)[1:-1]})")
        else:
            self.execute(
                f"INSERT INTO {table} VALUES ({str(values)[1:-1]})"
                f"where={where}"
            )

    def grant_permissions(self, *permissions, user, host, sql_obj):
        if len(permissions) == 0:
            commons.logger.warn(
                "Attempted to GRANT permissions without specifying them"
            )
            return -1

        sql_query = "GRANT %s ON %s TO '%s'@'%s'" % (
            ", ".join(permissions),
            sql_obj,
            user,
            host,
        )

        commons.logger.info(
            "permissions %s granted for '%s'@'%s' on %s"
            % (permissions, user, host, sql_obj)
        )

        self.execute(sql_query)

    def revoke_permissions(self, user, host, sql_obj, *permissions):
        if len(permissions) == 0:
            commons.logger.warn(
                "Attempted to GRANT permissions without specifying them"
            )
            return -1
        sql_query = "REVOKE %s ON %s FROM %s@%s" % (
            ", ".join(p for p in permissions),
            sql_obj,
            user,
            host,
        )

        commons.logger.info(
            "permissions %s revoked for '%s'@'%s' on %s"
            % (permissions, user, host, sql_obj)
        )
        print(sql_query)
        self.execute(sql_query)

    def drop_user(self, user, host):
        self.execute(f"DROP USER '{user}'@'{host}'")

    def create_user(self, user, host, password):
        self.execute(f"CREATE USER '{user}'@'{host}' "
                     f"IDENTIFIED BY '{password}'")
