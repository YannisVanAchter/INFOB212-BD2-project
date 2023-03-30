# encoding uft-8
import mysql.connector
from time import sleep

def main():
    print("Hello, world!")
    print("Helle Aline :)")
    print("Hello Loulou")
    sleep(3)
    db = mysql.connector.connect(user='user', passwd='password', host='localhost', database='mysql')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM *")

    for row in cursor.fetchall():
        print(row)

if __name__ == "__main__":
    main()
