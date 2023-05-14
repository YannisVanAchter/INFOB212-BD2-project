# encoding uft-8
# we could use cs50 module for it but we would need to import Falsk and other package that we won't use
"""
module that provide useful function for the input of user
"""

from datetime import date as Date
from typing import Type

from .database import DataBase

def get_string(prompt: str = "") -> (str):
    """ask to user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request show to user. Defaults to "")->(str.

    Return:
    -------
        str: answer of user
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Yannis Van Achter
    """
    try:
        return input(prompt)
    except EOFError:
        return None
    
def get_date(prompt: str = "", before: Date = None, after: Date = None) -> (Date):
    """ask to user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request shows to user. Defaults to ""
        before (Date, optional): date before. Defaults to None
        after (Date, optional): date after. Defaults to None

    Return:
    -------
        Date: answer of user
        
    Version:
    --------
        1.0.0
    
    Author:
    -------
        Yannis Van Achter
    """
    date_input = None
    while date_input == None or (before != None and date_input < before) or (after != None and date_input > after):
        try:
            date_input = Date.fromisoformat(get_string(prompt))
        except (TypeError, ValueError):
            pass
    return date_input
    
def get_float(prompt: str = "") -> (float):
    """ask to user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request shows to user. Defaults to "")->(str.

    Return:
    -------
        float: answer of user
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Yannis Van Achter
    """
    while True:
        try:
            return float(get_string(prompt))
        except (TypeError, ValueError):
            pass
        
def get_int(prompt: str = "") -> (int):
    """ask user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request show to user. Defaults to "")->(str.

    Return:
    -------
        int: answer of user
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Yannis Van Achter
    """
    while True:
        try:
            return int(get_string(prompt))
        except (TypeError, ValueError):
            pass
        
        
def get_sql_user_querry(prompt: str = "") -> (str):
    """Ask to user for personnal sql querry

    Args:
    -----
        prompt (str): Request shows to user
        
    Return:
    -------
        str: sql querry user writed
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Yannis Van Achter
    """
    querry = ""
    print(prompt, end="")
    while not querry.strip().endswith(";"):
        querry += get_string()
        
    return querry

def get_valid_id(db: DataBase, prompt: str, table_name: str) -> int:
    """Ask user for valid id in database

    Args:
    -----
        db (DataBase): database to check id, 
            connect with user that have SELECT grant permission on table_name
        prompt (str): Request to user.( ce qui est affiché à l'utilisateur)
        table_name (str): Name of table to check id.
      
    Raises:
    -------
        TypeError: if id_type is not int or str

    Return:
    -------
        id : valid id
        id = None : if id is not valid (not found in "mysql".table)
        
    Version:
    --------
        2.0.0
        
    Author:
    -------
        Yannis Van Achter
        Aurélie Genot & Youlan Collard
    """

    try:
        id = get_int(prompt)
        db.execute_with_params(f"SELECT id from {table_name} where id = %s; ", [id])
        if len (db.tableArgs) == 0: 
            id = None 
            print("ERROR: id not found")
        return id
    except (TypeError, ValueError):
        pass
    

    