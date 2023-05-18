# encoding: utf-8

from module.get import get_float


def ask_blood_quantity(limit: int = None) -> (float):
    """ask user to enter the blood quantity

    Arg:
    ----
        limit (int, optional): limit that we will not cross. Defaults to None.

    Return:
    -------
        float: quantity of blood input by user
    """
    quantity = -1
    while 0 > quantity or (limit is not None and (quantity >= limit)):
        quantity = get_float("Enter the blood quantity: ")
    return quantity


def ask_price(prompt: str = None) -> (float):
    """ask user to enter the price

    Args:
    -----
        prompt (str, optional): request to user. Defaults to None.

    Return:
    -------
        float: price input by user
        
    Author:
    -------
        Yannis Van Achter
    """
    if prompt is None:
        prompt = "Enter the price: "

    price = -1
    while price <= 0:
        price = get_float(prompt)
    return price
