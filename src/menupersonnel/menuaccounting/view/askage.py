# encoding: utf-8

from module.get import get_float


def ask_age_of_death() -> (float | int):
    """Ask the age of death of the donor.

    Return:
    -------
        float: The age of death of the donor.
    """
    age = -1
    while not (0 < age < 150):
        age = get_float("Enter the age of death: ")
    return age
