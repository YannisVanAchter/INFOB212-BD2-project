from module.get import *
from contants import * 

def main_persoadmin_menu ():
    """
    
    """

    organe_choice = get_string(print("You are there for a transplantation on which organe?", f"List of organes: {ORGAN_LIST}"))

    input_valid = False
    while not input_valid:
        organe_choice = get_int("")

        if organe_choice == "lung":
            input_valid = True
            pass
        elif organe_choice == 2:
            input_valid = True
            pass
        else:
            print("Votre sélection n'est pas valide, réessayez.")
    

















"""
 print("Have you passed an order for a transplantation or delivery ?")
    print("Enter 1 if it is a transplantation")
    print("Enter 1 if it is a order")
    choice = get_int(print("What is your choice ?"))


    input_valid = False
    while not input_valid:
        if choice == 1:
            input_valid = True

            
        elif choice == 2:
            input_valid = True
            
            
        else:
            print("Your selection is not valid, please start from the beginning idiot")

"""
