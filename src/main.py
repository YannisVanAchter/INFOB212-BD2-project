# encoding uft-8

# import
# native
from time import sleep

# pip install -r requerements.txt
import mysql.connector

# local modules
from exception.unconnectederror import UnConnectedError

def db_connect(user, password, host, database):
    # TODO: specify + place type hinting
    db = mysql.connector.connect(user=user, passwd=password, database=database, host=host)
    if not db.is_connected():
        raise UnConnectedError()
    
    cursor = db.cursor()
        
    return db, cursor

def db_disconnect(db, cursor):
    # TODO: specify + place type hinting
    cursor.close()
    db.disconnect(cursor)

def main():
    db, cursor = db_connect(user='root', passwd='password', host='mysql', database='mysql')

    # TODO: remove until db_disconnect()
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
