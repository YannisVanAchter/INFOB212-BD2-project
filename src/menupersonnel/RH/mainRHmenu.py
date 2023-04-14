from module.database import DataBase
from module.get import get_int 
from module.get import get_bool
from module.get import get_string 

def main_RH_menu(database: DataBase):
    """
    Menu for HR. 
    
    allow the person of HR to: 
    --------------------------
    - Add employee
    - Modify employee
    - Delete employee 

    Args:
        database (DataBase): Data base connected for HR 
    """
   
    print("In RH menu")
    validity = False

    while (validity == False): 
        print("Choose what you want to do: ")
        print("Type 0 if you want add an employee to the company ")
        print("Type 1 if you want to modify an actual employee ")
        print("Type 2 if you want to delete an actual employee ")
        choice = get_int("your choice: ")
        if (choice != 0 and choice != 1 and choice != 2):
            validity = False 
            print("This operation is not possible, please choose another number")
        else: 
            validity = True 
    
    # According to the number choosen, will display the good choice
    
    if choice == 0:
        add_employee()
    
    if choice == 1: 
        modify_employee()
        
    if choice == 2: 
        delete_employee()


def add_employee():
    """ 
    To add a new employee
    """
    DataBase.connect()
    print("You have choosen to add a new employee")
    existence = get_bool("Does this new employee is already register in our system ? Enter 0 if no and 1 if yes ")
    
    DataBase.disconnect()
    
def modify_employee(): 
    """_
    To modify an actual employee (to change his function)
    """
    print("Modify bien appelé")
    
def delete_employee(): 
    """
    To delete an employee of the 
    """
    print("delete bien appelé")