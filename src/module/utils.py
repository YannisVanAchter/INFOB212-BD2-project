# encoding uft-8
import logging
import os
from datetime import date as Date

from module.database import DataBase
from module.get import get_valid_id


def clear_terminal():
    """clear terminal"""
    command = 'clear'
    if os.name in ('nt', 'dos'): # Windows
        command = 'cls'
    os.system(command)


def insert_into(database: DataBase, table: str, attributes: tuple[str], values: tuple):
    """insert into database

    Args:
    -----
        database (DataBase): DataBase to insert, connect for this user
        table (list[str]): table where insert
        attributes (tuple[str]): attributes to insert
        values (tuple): values to insert
        
    Raises:
    -------
        TypeError: if database is not a DataBase
        TypeError: if table is not a str
        TypeError: if attributes is not a tuple or list
        TypeError: if values is not a tuple or list
        ValueError: if attributes and values have not the same length
        TypeError: if attributes[id] is not a str
    
    Return:
    -------
        int: id of the inserted row, if -1 ==> Errored in row insert
    """
    # test on args
    if not isinstance(database, DataBase):
        raise TypeError(f"database must be a DataBase not {type(database)}")
    if not isinstance(table, str):
        raise TypeError(f"table must be a str not {type(table)}")
    if not isinstance(attributes, (tuple, list)):
        raise TypeError(f"attributes must be a tuple or list not {type(attributes)}")
    if not isinstance(values, (tuple, list)):
        raise TypeError(f"values must be a tuple or list not {type(values)}")
    if len(attributes) != len(values):
        raise ValueError(f"attributes and values must have the same length not {len(attributes)} and {len(values)}")
    for id in range(len(attributes)):
        if not isinstance(attributes[id], str):
            raise TypeError(f"attributes[{id}] must be a str not {type(attributes[id])}")
    
    # init
    inserted_id = -1
    def to_string(x):
        if isinstance(x, str):
            return f"'{x}'"
        if isinstance(x, Date):
            return f"'{x.strftime('%Y-%m-%d')}'"
        if isinstance(x, bool):
            return str(int(x)).lower()
        return str(x)
    
    def value_type(x):
        r = '%s'
        if isinstance(x, (str, Date)):
            r = '%s'
        if isinstance(x, (int, float, bool)):
            r = '%i'
        return r
    
    # convert all values to string
    value_typed = ["%s" for _ in range(len(values))]
    # values = list(map(to_string, values))
    table = table.upper()
    if table == "ORDER":
        table += "_" # table 'ORDER' is also a key word in SQL we use '_' to the end to make the difference
    
    # create querry
    querry = f"INSERT INTO {table} ({', '.join(attributes)}) VALUES ({', '.join(value_typed)});"
    logging.info(f"Querry: {querry}")
    logging.info(f"Values: {values}")
    # execute querry
    with database as db:
        inserted_id = db.execute_with_params(querry, values)
        
    return inserted_id
        
    
def select_and_print_choice(database: DataBase, querry: str, information_selected: list[str], table: str) -> (int):
    """Use querry to select the expected information
    and print it with information_selected as header of table
    Allow user to input an id and return it if it is valid (id from table)

    Args:
    -----
        database (DataBase): database to check id, 
            connect with user that have SELECT grant permission on table_name
        querry (str): querry to select a list of employee
        information_selected (list[str]): list of information to print
        table (str): name of the table to check id
       
    Raises:
    -------
        TypeError: if id_type is not int or str

    Return:
    -------
        id : valid id
        id = None : if id is not valid (not found in "mysql".table)
        
    Version:
    --------
        1.0.0
    
    Author:
    -------
        Yannis Van Achter
    """
    print_selection(database, querry, information_selected)
    
    id = None
    while id is None:
        id = get_valid_id(database, "Enter the id: ", table)
    return id

def print_selection(database: DataBase, querry: str, information_selected: list[str]):
    def string_len(string, length):
        """Return string with length characters

        Args:
        -----
            string (str): string to check
            length (int): length of the string

        Return:
        -------
            string (str): string with length characters
        """
        if len(string) > length:
            string = string[:length]
            return string[:-3] + "..."
        else:
            return string + " " * (length - len(string))
    
    with database as db:
        db.execute(querry)
        information_list = db.table
    
    if len(information_list) == 0:
        print("No more information found")
    
    table_head = "| " + " | ".join(information_selected) + " |"
    separator = "+-" + "-+-".join(["-"*len(i) for i in information_selected]) + "-+"
    list_size = [len(i) for i in information_selected]
    
    print(table_head)
    print(separator)
    for information in information_list:
        print("| " + " | ".join(
            [string_len(str(string), list_size[i]) 
                for i, string in enumerate(information)
            ]
            ) + " |")
    print(separator)