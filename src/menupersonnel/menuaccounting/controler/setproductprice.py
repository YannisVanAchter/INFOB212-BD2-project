# encoding uft-8

from module import *
from menupersonnel.menuaccounting.contants import TABLE_FOR_PRICE_UPDATES 

def set_product_price(database: DataBase, price: float, product_id: int, table: str):
    """define the price of a product (already created)

    Args:
    -----
        database (DataBase): The data base to update/set
        price (float): price of the product (strictly positive)
        product_id (int): id of the product (strictly positive)
        table (str): the table to update (ORGANE, SANG, TYPE_LIVRAISON, TRANSPLATATION)
    """
    # check pre-condition 
    if not isinstance(database, DataBase):
        raise TypeError("database must be the type of DataBase")
    if price <= 0:
        raise ValueError("price must be positive")
    if product_id <= 0:
        raise ValueError("product_id must be positive")
    if table not in TABLE_FOR_PRICE_UPDATES:
        raise ValueError(f"table must be one of the following: {TABLE_FOR_PRICE_UPDATES[0]}" + ", ".join(TABLE_FOR_PRICE_UPDATES[1:]))

    # SQL update in data base
    with database as db:
        db.execute(f"UPDATE {table} SET price={price} WHERE id={product_id};")
