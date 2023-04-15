from module.database import DataBase
from module.get import get_int 
from module.get import get_bool
from module.get import get_string 
from menuconnexion.menu import main_login_menu

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
   
    print("You are now in HR menu")
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
    
    # According to the number choosen, will redirect to the good function
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
    existence = get_bool("Does this new employee is already register in our system ? Enter False if no and True if yes ")
    if existence == True: 
        create_person() 
    
    else : 
        id_person = get_int("Please enter the id of the person: ")
        if id_person not in (SELECT id FROM PERSON): ## A revoir
            print("This person doesn't exist")
        else: 
            create_employee(id)
        
    DataBase.disconnect()
    
def create_person(): 
    """
    To add a new employee who hasn't already created an account in the company. 
    Create a new account and call the function create_employee(id) with the id created
    """
    main_login_menu(database: DataBase) ## Appelle la fonction de Youlan pr la création d'un compte 
    ## On crée nous-même un compte employée mais du coup en théorie on génère ici un mdp temporaire que la personne devra changer 
    id_person = get_int("Please enter the id of the person: ")
    create_employee(id_person)


def create_employee(id): 
    """
    To add to a person who has already created an account in the company the role of employee 
    
    Args: 
    id : the id of the person that has already had an account in the company 
    """
    print("Now you will give the job of the user with this id")
    
            id_transplantation = input("Pouvez vous me donner l'identifiant de la transplantation dont vous souhaitez voir les organes?")

        # use 3*" your querry 3*", that will provide only one string
        #
        # Example:
        # organes = ("""SELECT etat, methode_de_conservation, type FROM ORGANE WHERE id_organe in
        # (SELECT id_organe FROM TRANSPLANTATION WHERE id_transplantation = %s)""")
        organes = ("SELECT etat, methode_de_conservation, type FROM ORGANE WHERE id_organe in"
        "(SELECT id_organe FROM TRANSPLANTATION WHERE id_transplantation = %s)")
        database.execute(organes, (id_transplantation))
    
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