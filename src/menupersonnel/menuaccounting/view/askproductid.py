# encoding uft-8

from module.get import get_int

def ask_product_id() -> (int):
    """ask user to enter the product id

    loop since user did not enter an correct product id

    Return:
    -------
        int: id of product
    """
    product_id = -1
    while product_id < 0:
        product_id = get_int("Enter the product id: ")
    return product_id