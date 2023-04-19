from module.database import DataBase
from module.get import get_int 
from module.get import get_bool
from module.get import get_string 
from module.get import get_valid_id 
from menuconnexion.menu import main_login_menu


def main_RH_menu(db: DataBase):
    """
    Menu for HR. 
    
    allow the person of HR to: 
    --------------------------
    - Add employee
    - Modify employee
    - Delete employee 

    Args:
        db (DataBase): Data base connected for HR 
    """
   
    print("You are now in HR menu")
    
    validity = True 

    def print_menu():
        print("Choose what you want to do: ")
        print("Type 0 if you want add an employee to the company ")
        print("Type 1 if you want to modify an actual employee ")
        print("Type 2 if you want to delete an actual employee ")
        print("Type 3 if you want to exit")


    while (validity == True): 
    
        print_menu()
        choice = get_int("your choice: ")
        if (choice not in {0,1,2,3}):
            print("This operation is not possible, please choose another number")
        else: 
            db.connect()
            if choice == 0: 
                add_employee()
            
            if choice == 1: 
                modify_employee()
                
            if choice == 2: 
                delete_employee()
            
            if choice == 3: 
                validity = False 

            db.disconnect()

def add_employee(db : DataBase):
    """ 
    To add a new employee
    Use the function create_person() and the function create_employee(id)
    
    Args:
    db (DataBase): Data base connected for HR 
    """
    
    db.connect()
    print("You have choosen to add a new employee")
    existence = get_bool("Does this new employee is already register in our system ? Enter False if no and True if yes ")
    
    if existence == True: 
        create_person() 
    
    else : 
        id_person = get_int("Please enter the id of the person: ")
        create_employee(id_person)
        
    db.disconnect()
    
def create_person(db : DataBase): 
    """
    To add a new employee who has not already created an account in the company. 
    Create a new account and call the function create_employee(id) with the id created
    
    Args:
    db (DataBase) : Data base connected for HR
    """
    main_login_menu(db) ## Appelle la fonction de Youlan pr la création d'un compte 
    ## On crée nous-même un compte employée mais du coup en théorie on génère ici un mdp temporaire que la personne devra changer 
    id_person = get_valid_id(db, "Please enter the id of the person:", "PERSON" , int)
    create_employee(id_person, db)

def create_employee(id, db: DataBase): 
    """
    To add to a person who has already created an account in the company the role of employee 
    
    Args: 
    id : the id of the person that has already had an account in the company 
    db (DataBase): Data base connected for HR 
    """
    db.connect()
    
    print("Now you will give the job of the user with this id")

    salary_person = get_int("Please enter the salary of the person: ")
    function_person = get_string("Please enter the exact function of the person in the company: ")
   
    db.execute(f"INSERT INTO STAFF (id, salary, function) VALUES ({id}, {salary_person}, {function_person})")
    
    print("Choose the category of the person: ")
    print("Type 0 if the person is an anaesthetist")
    print("Type 1 if the person is a nurse")
    print("Type 2 if the person is a doctor")
    print("Type 3 if the person is an accountant")
    print("Type 4 if the person is a HR person")
    print("Type 5 if the person is a CEO")
    print("Type 6 if the person does not belong to a particular category")
    
    category = get_int("The number of the category is: ")
    
    if category not in {0,1,2,3,4,5,6} :
        print("The number entered is not valid")
    else: 
        if category == 0:
            inami = get_string("Enter the INAMI number of the person:")
            db.execute(f"INSERT INTO ANAESTHETIST (id,inami_number) VALUES ({id},{inami})")
        if category == 1: 
            db.execute(f"INSERT INTO NURSE (id) VALUES ({id})")
        if category == 2: 
            inami = get_string("Enter the INAMI number of the person:")
            db.execute(f"INSERT INTO DOCTOR (id,inami_number) VALUES ({id},{inami})")
        if category == 3: 
            db.execute(f"INSERT INTO ACCOUNTANT (id) VALUES ({id})")  
        if category == 4: 
            db.execute(f"INSERT INTO HR (id) VALUES ({id})")  
        if category == 5: 
            db.execute(f"INSERT INTO CEO (id) VALUES ({id})")  
            
    db.disconnect()
            
def modify_employee(db : DataBase): 
    """_
    To modify an actual employee (to change his function)
    
    Args:
    db (DataBase): Data base connected for HR 
    """
    db.connect()
    
    id_employee = get_valid_id(db, "Please enter the id of the employee:", "STAFF" , int)
    
    print("What do you want to do?")
    choice = get_int("Type 1 if you want to modify the salary of the employee and 2 if you want to modify his function:")
    
    if choice not in {1,2}:
        print("Please enter a valid integer")
    else: 
        if choice == 1: 
            new_salary = get_int("Enter the new salary: ")
            db.execute(f"UPDATE salary = {new_salary} FROM STAFF WHERE ID = id_employee") 
        if choice == 2: 
            new_function = get_string("Enter the new function: ")
            db.execute(f"UPDATE function = {new_function} FROM STAFF WHERE ID = id_employee")
    
    db.disconnect()
    
def delete_employee(db: DataBase): 
    """
    To delete an employee 
    
    Args: 
    db (DataBase): Data base connected for HR 
    """
    db.connect()
    
    id_employee = get_valid_id(db, "Please enter the id of the person:", "STAFF" , int)

    print("Are you sure to delete this employee? After that you cannot go back ")
    confirmation = get_string("Type yes if you want to delete this person or no otherwise")
    
    if confirmation == "yes": 
        #Verifier si la personne n'est pas medecin, infirmiere ou anesthésiste 
        db.execute("SELECT id FROM MEDECIN")
        medecins = db.table
        db.execute("SELECT id FROM NURSE")
        medecins += db.table 
        db.execute("SELECT id FROM ANAESTHETIST")
        medecins += db.table
        
        if id_employee not in medecins:
            db.execute("SELECT id FROM CEO")
            ceo = db.table
            if id_employee not in ceo:
                db.execute(f"DELETE id FROM STAFF WHERE id = {id_employee} ") # La personne devra supprimer son compte personne elle-même 
            else:
                print("You don't have the permission to delete the CEO")  
        else:
            db.execute("SELECT id FROM TRANSPLANTATION")
            transplantation_medecins = db.table 
            
            if id_employee not in transplantation_medecins:
                db.execute(f"DELETE id FROM STAFF WHERE id = {id_employee}")
            else: 
                print('This person can not be actually deleted because she works on a transplantation')       
    else: 
        print('This person will not be delete')
        
    db.disconnect()