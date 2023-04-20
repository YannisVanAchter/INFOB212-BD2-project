# encoding uft-8
"""Setup the database by reading the ddl file and executing its content"""

__author__ = "Yannis Van Achter"
__version__ = "INCOMPLETE AND TO FIX"

import logging
import sys
import time

from module.database import DataBase
from module.utils import clear_terminal

CONFIG = {
    'host': '127.0.0.1', 
    'user': 'root', 
    'password': 'password', 
    'database': 'mysql', 
    'port': 3306,
    # 'auto_commit': True, 
    'auto_connect': True,
}

def __init_database__():
    """Init database by inserting values"""
    # define constants for main function
    database_sql_file = "../sql/DB2-Project-Adopte-ton-mort.ddl"
    
    db = DataBase(**CONFIG)
    
    with open(database_sql_file, 'r') as f:
        db.execute(f.read(), multi=True)
        logging.debug(f"Executed {database_sql_file} file")
    time.sleep(5) # make sure MySQL executes all statements to generate the database
        
    # db.commit()
    
    # Test that the database has been created
    query = "SHOW tables;"
    
    logging.debug(f"Try: {query}")
    db.execute(query)
    logging.debug(f"Executed")
    
    for row in db.table:
        logging.debug(f"Fetched row: {row}")
        
    # db.commit()
    # db.disconnect()
    logging.info('Database successfully created')
            
if __name__ == "__main__":
    if '-w' in sys.argv or '--warning' in sys.argv:
        print("Running with warning log level")
        set_level  = logging.WARNING
        
    if '-d' in sys.argv or '--debug' in sys.argv:
        print("Running with debug log level")
        set_level = logging.DEBUG
        
    elif '-i' in sys.argv or '--info' in sys.argv:
        print("Running with info log level")
        set_level = logging.INFO
        
    else: 
        set_level = 0
        
    logging.basicConfig(
        level=set_level, 
        format="%(asctime)s.\nLog level: %(levelname)s \n%(message)s\n\n"
    )
    __init_database__()
    
    # if set_level in [0, logging.INFO]:
    #     clear_terminal()
        
    # automatically start application
    if 'launch' in sys.argv:
        import main 
        main.main()
    