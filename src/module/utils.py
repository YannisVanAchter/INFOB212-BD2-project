# encoding uft-8

import os
from datetime import datetime as DateTime, date as Date

from module.database import DataBase


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
        if not isinstance(x, str):
            return str(x)
        else:
            return f"'{x}'"
    
    # convert all values to string
    values = list(map(to_string, values))
    table = table.upper()
    
    # create querry
    querry = f"INSERT INTO {table} ({', '.join(attributes)}) VALUES ({', '.join(values)})"
    
    # execute querry
    with database as db:
        db.execute(querry)
        inserted_id = db.last_row_id
        
    return inserted_id
        
    
