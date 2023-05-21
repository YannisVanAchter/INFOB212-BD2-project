# encoding uft-8

# import
import logging
import sys

# local modules
from module.database import DataBase
from module.utils import clear_terminal
from menuconnexion import main_login_menu

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
    try:
        main()
    except KeyboardInterrupt:
        clear_terminal()
        print("Hope to see you soon 🙂")
        sys.exit(0)
