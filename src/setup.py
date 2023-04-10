# encoding uft-8
"""Setup the database by reading the ddl file and executing its contents"""

__author__ = "Yannis Van Achter <discord:Yannis Van Achter#1444"
__version__ = "INCOMPLETE AND TO FIX"

import os
import logging
import sys

from module.database import DataBase
from module.utils import clear_terminal

CONFIG = {
    'host': '127.0.0.1', 
    'user': 'root', 
    'password': 'password', 
    'database': 'mysql', 
    'port': 3306,
    'auto_commit': True, 
    'auto_connect': True
}

def __init_database__():
    """Init database by insert values"""
    # define constants for main function
    temp_sql_file = './temp.sql'
    database_sql_file = "../sql/DB2-Project-Adopte-ton-mort.ddl"
    
    # with key word: https://www.geeksforgeeks.org/with-statement-in-python/
    logging.info(f"Start copying ddl project from {database_sql_file} to {temp_sql_file}")
    # read .ddl file and create a copy cleaned to make sure each line is a single sql query
    with open(database_sql_file, "r") as ddl:
        # use write only to overwrite existing lines if program crashed previously
        sql = open(temp_sql_file, "w") 
        
        # init while loop to manage triggers: check further
        # lines = ddl.readlines()
        # line_index = 0
        # while line_index < len(lines):
        #     line = lines[line_index]
        #     line_index += 1
        for line in ddl.readlines():
            if line.strip().startswith("--") or line == "\n":
                continue # skip empty lines and comments lines
            
            logging.debug(f"brut line: {line}")
            no_line_break = line.replace("\n", " ")
            logging.debug(f"no line break: {no_line_break}")
            
            striped = no_line_break.strip(" ") # remove empty spaces before and after line
            logging.debug(f"striped: {striped}")
            
            # Manage when we have a trigger statement that has many ';'
            # if ( # TODO: use regex instead
            #     striped.startswith("create Trigger") 
            #     or striped.startswith("create trigger")
            #     ) and line_index < len(lines):
            #     logging.debug("Trigger statement management is running.")
            #     while not striped.endswith("end;"):
            #         new_line = lines[line_index]
            #         line_index += 1
            
            #         logging.debug(f"New line in trigger statement: {new_line}")
            #         no_line_break = new_line.replace("\n", " ")
                    
            #         # add new line to trigger statement line for temporary file
            #         striped += no_line_break.strip(" ")
                    
            #     logging.debug("Trigger statement successfully managed")
            
            sql_querry = striped.replace(";", ";\n") # because this is the end of a sql query
            logging.debug(f"sql querry: {sql_querry}")
            
            sql.write(sql_querry)
        
        sql.close()

    logging.info("Start executing sql statements in containered database")
    with open(temp_sql_file, "r") as file:
        init: list[str] = file.readlines()
        
        with DataBase(**CONFIG) as db:
            for query in init:
                sql_query = query.replace("\n", " ")
                
                logging.debug(f"Final query executed: {sql_query}")
                db.execute(sql_query)
                logging.debug("Execution succeeded\n")

    os.remove(temp_sql_file)
    logging.info(f"Removing temporary file: {temp_sql_file}")
    logging.info("End of process")
            
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
        set_level = -1
        
    logging.basicConfig(level=set_level)
    __init_database__()
    
    if set_level in [0, logging.INFO]:
        clear_terminal()
    