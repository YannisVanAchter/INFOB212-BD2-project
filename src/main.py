# encoding uft-8

# import
# native

# pip install -r requerements.txt
import mysql.connector as mysql

# # local modules
# from menupersonnel.menuaccounting import main_accounting_menu
# from menupersonnel.menumédecin import main_medecin_menu
# from menupersonnel.RH import main_RH_menu
# from module.database import DataBase

# function and class
def main():
    # database = DataBase(user='user', password='password', host='localhost:3306', database='mysql')
    # database.connect()
    cnx = mysql.connect(
        host='127.0.0.1', 
        username='user', 
        passwd='password', 
        database='mysql',
        port=3306
    )
    cursor = cnx.cursor()

    # TODO: create test for db_disconnect() and db_connect() with it
    cursor.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER(64) PRIMARY KEY, name VARCHAR(255))")

    cursor.execute("INSERT INTO test VALUES (2, 'bla')")
    cursor.execute("INSERT INTO test VALUES (3, 'blabla')")
    cursor.execute("INSERT INTO test VALUES (4, 'blablabla')")
    cursor.execute("SELECT * FROM test")

    for row in cursor.fetchall():
        print(row)
        
    # database.disconnect()
    
    # main_accounting_menu(database)
    # main_medecin_menu(database)
    # main_RH_menu(database)
    
    cursor.close()
    cnx.disconnect()

if __name__ == "__main__":
    main()
