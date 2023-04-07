# encoding uft-8
"""Provide user request for "what type of product is it: " """
__author__  = "Yannis Van Achter"
__date__    = "06 april 2023"
__version__ = "1.0.0"

from module.get import  get_string

from menupersonnel.menuaccounting.contants import PRODUCT_LIST

def ask_product_type() -> (str):
    """ask user to enter the product type

    loop since user did not enter an correct product type

    Return:
    -------
        str: type of product
    """
    product_type = ""
    
    while product_type not in PRODUCT_LIST:
        product_type = get_string("Enter the product type: ")
        
    return product_type