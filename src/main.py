# encoding uft-8

# import
import logging, sys

# pip install -r requerements.txt
import mysql.connector as mysql

# # local modules
from menupersonnel.menuaccounting import main_accounting_menu
from menupersonnel.menumédecin import main_medecin_menu
from menupersonnel.RH import main_RH_menu
from menupersonnel.menupersonneladministratif import main_persoadmin_menu
from module.database import DataBase
from auth import login, register

# function and class
def main():
    print("Hello, world!")
    print("Helle Aline :)")
    print("Hello Loulou :)")

    
    with DataBase(
                host='localhost', 
                user='user', 
                password='password', 
                database='mysql',
                port=3306,
                auto_connect=True,
        ) as database:
        address = {
            'street': 'Route',
            'number': 1,
            'postalCode': 6000, 
            'city': "Paris", 
            "land": "France"
        }
        register(database, "test@gmail.com", "test", "password", "12/12/2000", address, "A", "+")
        login(database, "test@gmail.com", "password")

    #     # TODO: create test with it
    #     database.execute(
    #         "CREATE TABLE IF NOT EXISTS test(id INTEGER(64) unsigned AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))"
    #         )

    #     database.execute_many(
    #         "INSERT INTO test (name) VALUES ( 'bla')",
    #         "INSERT INTO test (name) VALUES ( 'blabla')",
    #         "INSERT INTO test (name) VALUES ( 'blablabla')")
    #     database.execute("SELECT * FROM test")

    #     for row in database.table:
    #         print(row)
    main_persoadmin_menu()


if __name__ == "__main__":
    if '-d' in sys.argv:
        logging.basicConfig(
            level=logging.DEBUG
        )
    elif '-i' in sys.argv:
        logging.basicConfig(
            level=logging.INFO
        )
    else:
        logging.basicConfig(
            level=logging.WARNING,
            filename='./app.log',
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    main()
