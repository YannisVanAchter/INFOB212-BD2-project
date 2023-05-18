# encoding: utf-8

from module.get import get_string


def ask_organ_conservation_method() -> (str):
    """Ask user to enter the organ conservation method

    Return:
    -------
        str: organ conservation method input by user
        
    Author:
    -------
        Yannis Van Achter
    """
    temp = "not null"
    method = ""

    print("Enter the organ conservation method: ")
    while temp != "":
        temp = get_string().strip()
        method += temp + "\n"

    if len(method) > 64:
        print("Method must be 64 characters or less")
        return ask_organ_conservation_method()

    return method
