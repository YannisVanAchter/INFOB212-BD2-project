# encoding uft-8
# we could use cs50 module for it but we would need to import Falsk and other package that we won't use
"""
module that provide useful function for input of user
"""
__version__ = "1.0.0"
__author__ = "yannis van achter <discord:Yannis Van Achter#1444"

from datetime import date as Date
from typing import Type

from .database import DataBase

def get_string(prompt: str = "") -> (str):
    """ask user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request show to user. Defaults to "")->(str.

    Return:
    -------
        str: response of user
        
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
    """ask user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request show to user. Defaults to ""
        before (Date, optional): date before. Defaults to None
        after (Date, optional): date after. Defaults to None

    Return:
    -------
        Date: response of user
        
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
    
    
def get_float(prompt: str = "") -> (float):
    """ask user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request show to user. Defaults to "")->(str.

    Return:
    -------
        float: response of user
        
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
        int: response of user
        
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
        
def get_bool(prompt: str = "") -> (bool):
    """ask user a request and get input of answer

    Args:
    -----
        prompt (str, optional): request show to user. Defaults to ""

    Return:
    -------
        bool: response of user
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Yannis Van Achter
    """
    while True:
        try:
            return bool(get_string(prompt))
        except (TypeError, ValueError):
            pass
        
def get_sql_user_querry(prompt: str = "") -> (str):
    """Ask user for personnal sql querry

    Args:
    -----
        prompt (str): Request to user
        
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

def get_valid_id(database: DataBase, prompt: str, table_name: str, id_type: Type = int) -> (int):
    """Ask user for valid id in database

    Args:
    -----
        database (DataBase): database to check id, 
            connect with user that have SELECT grant permission on table_name
        prompt (str): Request to user.( ce qui est affiché à l'utilisateur)
        table_name (str): Name of table to check id.
        id_type (Type, optional): type of id to check (int or str). Defaults to 'integer'
        
    Raises:
    -------
        TypeError: if id_type is not int or str

    Return:
    -------
        id_type(): valid id
        
    Version:
    --------
        1.0.0
        
    Author:
    -------
        Yannis Van Achter
    """
    if id_type not in (int, str):
        raise TypeError("id_type must be int or str")
    
    id_list = []
    with database as db:
        db.execute(f"SELECT id FROM {table_name};")
        id_list = db.table
        
    while True:
        try:
            id = id_type(get_string(prompt))
            if id not in id_list:
                raise ValueError
            return id
        except (TypeError, ValueError):
            pass
    