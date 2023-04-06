# encoding uft-8

from module.get import get_string, get_float, get_int, get_sql_user_querry
from module.database import DataBase
from module.utils import clear_terminal as cls

def main_accounting_menu(database: DataBase):
    """Accountent menu

    allow user to:
    --------------
        - set product price
        - update price
        - insert new product
        - research for accounting stuff
            - selling quantity
            - where are the clients
            - get price of each command
            - get/set price of delivery

    Args:
    -----
        database (DataBase): Data base connected for this user (the accountent)
    """
    cls()
    