# encoding uft-8

from module.get import get_float


def ask_product_price() -> (float):
    """ask user for product price

    return:
    -------
        float: price input by user
        
    Author:
    -------
        Yannis Van Achter
    """
    price = -1

    # check and loop if price is lower than 0
    while price <= 0:
        price = get_float("Enter the price of this product: ")

    return price
