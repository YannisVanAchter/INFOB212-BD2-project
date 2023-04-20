# encoding uft-8

import os


def clear_terminal():
    """clear terminal"""
    command = 'clear'
    if os.name in ('nt', 'dos'): # Windows
        command = 'cls'
    os.system(command)


# encoding: utf-8

from module.database import DataBase

def insert_into(database: DataBase, table: list[str], attributes: tuple[str], values: tuple):
    """insert into database

    Args:
    -----
        database (DataBase): DataBase to insert, connect for this user
        table (list[str]): table where insert
        attributes (tuple[str]): attributes to insert
        values (tuple): values to insert
    
    Return:
    -------
        int: id of the inserted row
    """
    id = -1
    querry = f"INSERT INTO {table} ({', '.join(attributes)}) VALUES ({', '.join(values)})"
    with database as db:
        db.execute(querry)
        id = db.last_row_id
        
    return id
        
    
