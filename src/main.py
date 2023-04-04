# encoding uft-8

# import
# native

# pip install -r requerements.txt
import mysql.connector as mysql

# local modules
from module.database import DataBase

# function and class
def main():
    database = DataBase(user='user', password='password', host='mysql', database='mysql')
    db, cursor = database.connect()

    # TODO: create test for db_disconnect() and db_connect() with it
    database.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER(64) PRIMARY KEY, name VARCHAR(255))")

    database.execute("INSERT INTO test VALUES (2, 'bla')")
    database.execute("INSERT INTO test VALUES (3, 'blabla')")
    database.execute("INSERT INTO test VALUES (4, 'blablabla')")
    database.execute("SELECT * FROM test")

    for row in database.table:
        print(row)
        
    database.disconnect()

if __name__ == "__main__":
    main()
