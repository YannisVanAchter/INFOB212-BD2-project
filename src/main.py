# encoding uft-8

# import
import logging
import sys
import time

# pip install -r requerements.txt
# import mysql.connector as mysql

# # local modules
from menupersonnel.menuaccounting import main_accounting_menu
# from menupersonnel.menumédecin import main_medecin_menu
# from menupersonnel.RH import main_RH_menu
# from menupersonnel.menupersonneladministratif import main_persoadmin_menu
from module.database import DataBase
from menuconnexion import main_login_menu
# from auth import login, register

# function and class
def main():
    logging.info("Start program...")
    logging.info("Level info ✅")
    logging.debug("Level debug ✅")
    logging.warning("Level warning ✅")
    logging.error("Level error ✅")
    logging.critical("Level critical ✅")
    
    with DataBase(
                host='localhost', 
                user='user', 
                password='password', 
                database='db',
                port=3306,
                auto_connect=True,
        ) as db:
        main_login_menu(db)


if __name__ == "__main__":
    if '-d' in sys.argv:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    elif '-i' in sys.argv:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    else:
        logging.basicConfig(
            level=logging.WARNING,
            filename='./app.log',
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    main()
