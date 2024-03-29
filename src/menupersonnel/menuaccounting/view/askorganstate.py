# encoding: utf-8

from module.get import get_string
from constants import ORGAN_STATE_LIST


def ask_organ_state() -> (str):
    """ask user to enter the organ state

    Return:
    -------
        str: organ state input by user
        
    Author:
    -------
        Yannis Van Achter
    """
    state = None
    print("Organ state that are valid:", ", ".join(ORGAN_STATE_LIST))
    while state not in ORGAN_STATE_LIST:
        state = get_string("Enter the organ state: ").strip().lower()
    return state
