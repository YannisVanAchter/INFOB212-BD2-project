from module.get import *
from contants import * 

def main_persoadmin_menu ():
    """
    
    """
    while True :
        organe_choice = get_string(print("You are there for a transplantation on which organe?", f"List of organes: {ORGAN_LIST}"))

        
        if organe_choice in ORGAN_LIST:
            print("Your selection is valid, thank you")
            break 
        
        else:
            print("Your selection is not valid, please start from the beginning idiot")
            continue

    
    date_choice = get_date(print("Enter a date for your operation"))
    print("Your operation will attend on %d", date_choice)


    










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
