# encoding uft-8

from module import *
from constants import TABLE_FOR_PRICE_UPDATES 

def set_product_price(database: DataBase, price: float, product_id: int|str, table: str):
    """define the price of a product (already created)

    Args:
    -----
        database (DataBase): The data base to update/set
        price (float): price of the product (strictly positive)
        product_id (int|str): id of the product (strictly positive if int and len <= 16 if str)
        table (str): the table to update (ORGANE, SANG, TYPE_LIVRAISON, TRANSPLATATION)
    """
    # simple function for clean code
    # more about lambda at: https://www.geeksforgeeks.org/python-lambda-anonymous-functions-filter-map-reduce/
    is_number = lambda x: isinstance(x, (int, float))
    is_string = lambda x: isinstance(x, str)
    is_valid_table = lambda t: t in TABLE_FOR_PRICE_UPDATES

    # check pre-condition
    if not isinstance(database, DataBase):
        raise TypeError("database must be the type of DataBase")
    if is_number(price) and price <= 0:
        raise ValueError("price must be a positive number")
    if not is_valid_table(table):
        raise ValueError(
            f"table must be one of the following: {TABLE_FOR_PRICE_UPDATES[0]}"
            + ", ".join(TABLE_FOR_PRICE_UPDATES[1:]) # only for visual
        )
    if (is_number(product_id) and product_id < 0) or (
        # check for table TYPE_DELIVERY
        is_string(product_id) and table == "TYPE_DELIVERY"  and len(product_id) <= 16
    ):
        raise ValueError(
            "product_id must be positive number or string with len <= 16, only if table is 'TYPE_DELIVERY'"
        )

    # SQL update in data base
    with database as db:
        db.execute(f"UPDATE {table} SET price={price} WHERE id={product_id};")

def _test():
    import unittest 
    
    # TODO: write tests
    
if __name__ == "__main__":
    _test()