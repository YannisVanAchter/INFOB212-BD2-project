# encoding uft-8
import mysql.connector
from time import sleep

def main():
    print("Hello, world!")
    print("Helle Aline :)")
    print("Hello Loulou")
    sleep(3)
    db = mysql.connector.connect(user='root', passwd='password', host='mysql', database='mysql')
    print(db.is_connected())

    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER(64) PRIMARY KEY, name VARCHAR(255))")

    cursor.execute("INSERT INTO test VALUES (2, 'bla')")
    cursor.execute("INSERT INTO test VALUES (3, 'blabla')")
    cursor.execute("INSERT INTO test VALUES (4, 'blablabla')")
    cursor.execute("SELECT * FROM test")

    for row in cursor.fetchall():
        print(row)

if __name__ == "__main__":
    main()
