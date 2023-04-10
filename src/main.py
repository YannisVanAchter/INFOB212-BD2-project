# encoding uft-8

# import
# native

# pip install -r requerements.txt
import mysql.connector as mysql

# # local modules
from menupersonnel.menuaccounting import main_accounting_menu
from menupersonnel.menumédecin import main_medecin_menu
from menupersonnel.RH import main_RH_menu
from module.database import DataBase

# function and class
def main():
    with DataBase(
                host='127.0.0.1', 
                user='root', 
                password='password', 
                database='mysql',
                port=3306,
                auto_connect=True,
                auto_commit=True,
        ) as database:

        # TODO: create test with it
        database.execute(
            "CREATE TABLE IF NOT EXISTS test(id INTEGER(64) unsigned AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))"
            )

        database.execute_many(
            "INSERT INTO test (name) VALUES ( 'bla')",
            "INSERT INTO test (name) VALUES ( 'blabla')",
            "INSERT INTO test (name) VALUES ( 'blablabla')")
        database.execute("SELECT * FROM test")

        for row in database.table:
            print(row)

if __name__ == "__main__":
    main()
