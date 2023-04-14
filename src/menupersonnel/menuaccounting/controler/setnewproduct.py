# encoding uft-8

from datetime import datetime

from module.database import DataBase

def create_new_organe(
        database: DataBase, 
        state: str, 
        functionnal: bool, 
        expiration_date: datetime, 
        method_of_conservation: str, 
        price: float|int,
        com_id: int,
        expiration_date_transplantation: datetime = None,
    ):
    """create new row in organe table

    Args:
        database (DataBase): database where insert
        state (str): state of conservation
        functionnal (bool): can be transplanted ?
        expiration_date (datetime): expiration for eating
        method_of_conservation (str): how do you conserve it ?
        price (float | int): how much is it, to get this organe
        com_id (int): who is the donnator
        expiration_date_transplantation (datetime, optional): when can't we transplant it ?. Defaults to None.
    """
    
    pass

def create_new_blood_row(
        database: DataBase,
        type: str,
        signe: bool,
        expiration_date: datetime,
        quantity: float|int,
        personn_donator: int = None,
        transplantation_usage: int = None
    ):
    """create new row in blood table

    Args:
        database (DataBase): database where insert
        type (str): check (A, B, O, AB)
        signe (bool): True: +, False: -
        expiration_date (datetime): when can't we drink it anymore ?
        quantity (float | int): _description_
        personn_donator (int, optional): _description_. Defaults to None.
        transplantation_usage (int, optional): _description_. Defaults to None.
    """
    pass