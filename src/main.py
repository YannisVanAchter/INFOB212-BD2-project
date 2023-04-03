# encoding uft-8

# import
# native
import time

# pip install -r requerements.txt
import mysql.connector as mysql
from mysql.connector.connection import MySQLConnection
from mysql.connector import CMySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor


# local modules
from exception.unconnectederror import UnConnectedError

def db_connect(user: str, password: str, host: str|int, database: str, **kwargs) -> (tuple[MySQLConnection|CMySQLConnection, CMySQLCursor]):
    """Connect to database and place cursor

    Args:
    -----
        user (str): user name to connect to database
        password (str): password to connect to database
        host (str|int): host to connect by container network in Docker
        database (str): database name to connect

    Raises:
    ------
        UnConnectedError: If database is not connected

    Returns:
    --------
        tuple (MySQLConnection|CMySQLConnection, CMySQLCursor): db, cursor
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Youlan Collart & Yannis Van Achter
    """
    db = mysql.connect(user=user, passwd=password, database=database, host=host, **kwargs)
    if not db.is_connected():
        raise UnConnectedError()
    
    cursor = db.cursor()
        
    return db, cursor

def db_disconnect(db: MySQLConnection|CMySQLConnection, cursor: CMySQLCursor) -> (None):
    """Disconnect to database and close cursor

    Args:
    -----
        db (MySQLConnection|CMySQLConnection): database instance
        cursor (CMySQLCursor): cursor instance
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Youlan Collart & Yannis Van Achter
    """
    cursor.close()
    db.disconnect()

def main():
    # time.sleep(10)
    db, cursor = db_connect(user='user', password='password', host='mysql', database='mysql')

    # TODO: create test for db_disconnect() and db_connect() with it
    cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER(64) PRIMARY KEY, name VARCHAR(255))")

    cursor.execute("INSERT INTO test VALUES (2, 'bla')")
    cursor.execute("INSERT INTO test VALUES (3, 'blabla')")
    cursor.execute("INSERT INTO test VALUES (4, 'blablabla')")
    cursor.execute("SELECT * FROM test")

    for row in cursor.fetchall():
        print(row)
        
    db_disconnect(db, cursor)

if __name__ == "__main__":
    main()
