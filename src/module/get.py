# encoding uft-8
# we could use cs50 module for it but we would need to import Falsk and other package that we won't use
"""
module that provide useful function for input of user
"""
__version__ = "1.0.0"
__author__ = "yannis van achter <discord:Yannis Van Achter#1444"

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