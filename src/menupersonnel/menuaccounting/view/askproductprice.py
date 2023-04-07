# encoding uft-8
"""Provide user request for "what is the price of this product: " """
__author__  = "Yannis Van Achter"
__date__    = "06 april 2023"
__version__ = "1.0.0"

from module.get import get_float

def ask_product_price() -> (float):
    """ask user for product price
    
    return:
    -------
        float: price input by user
    """
    price = -1
    
    # check and loop if price is lower than 0
    while price <= 0:
        price = get_float("Enter the price of this product: ")
        
    return price