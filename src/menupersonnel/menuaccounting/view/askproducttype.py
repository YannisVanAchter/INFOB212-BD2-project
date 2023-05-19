# encoding uft-8

from module.get import get_string

from constants import ORGAN_DICO, BLOOD_TYPE


def ask_product_type(is_organe: bool = False) -> str:
    """ask user to enter the product type

    loop since user did not enter an correct product type

    Return:
    -------
        str: type of product
        
    Author:
    -------
        Yannis Van Achter
    """
    product_type = ""

    if is_organe:
        while product_type not in ORGAN_DICO.keys():
            product_type = get_string("Enter the product type: ").lower().strip()
    else:
        while product_type not in BLOOD_TYPE:
            product_type = get_string(f"Enter the product type: ({'/'.join(BLOOD_TYPE)})").upper().strip()

    return product_type
