# encoding uft-8

# Import of the modules
import string
import random
import logging

from module.database import DataBase
from module.get import get_int, get_string, get_valid_id 
from auth.authenticate import register

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
    def print_menu():
        print("\n Choose what you want to do: ")
        print("Type 0 if you want add an employee to the company")
        print("Type 1 if you want to modify an actual employee ")
        print("Type 2 if you want to delete an actual employee ")
        print("Type 3 if you want to exit")
   
    logging.info("You are now in HR menu")
    print("Welcome in HR menu, here you can add, modify or delete an employee")

    validity = True 
    while validity: 
    
        print_menu()
        choice = get_int("your choice: ")
        db.connect()
        if choice == 0: 
            add_employee(db)
        elif choice == 1: 
            modify_employee(db)
        elif choice == 2: 
            delete_employee(db)
        elif choice == 3: 
            validity = False 
        else:
            print("This operation is not possible, please choose another number")

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
    
    ## Check if the person has already registered in our system
    existence = ""
    while (existence != "yes" and existence != "no"):
        existence = get_string("Does this new employee has already an account PERSON? Enter no or yes ")
        
    if existence == 'no': 
        create_person(db) 
    
    if existence == 'yes' : 
        id_person = get_valid_id(db, "Please enter the id of the person: ", "PERSON")
        create_employee(id_person, db)
        
    db.disconnect()
   
def create_person(db : DataBase): 
    """
    To add a new employee in the staff who has not already created an account in the company. 
    We create ourselves an account PERSON and we generate ourselves a temporary password.
    Call the function create_employee(id) with the id created
    
    Args:
    db (DataBase) : Data base connected for HR
    """
    
    print("Now you will create a new personnal account")
    email = get_string("Please enter the email of the person: ")
    last_name = get_string("Enter the last name of the person: ")
    first_name = get_string("Enter the first name of the person: ")
    phone_number = get_int ("Enter the phone number of the person: ")
    birth_date = get_string("Enter the date of birth of the person (DD/MM/YYYY): ")
    street = get_string("Enter the street of the address: ")
    number = get_string("Enter the number of the address: ")
    postalCode = get_int ("Enter the postal code of the addess: ")
    city = get_string("Enter the city: ")
    land = get_string("Enter the land: ")
    address = {"street" : street, "number" : number, "postalCode" : postalCode, "city" : city, "land": land }
    
    #Generate a temporary password for the new person 
    temporary_password = ""
    length_password = 8
    for _ in range (length_password):
        temporary_password += random.choice(string.ascii_letters + string.digits) 

    id_person = register(db,email, temporary_password, birth_date, address,  last_name, first_name, phone_number)
    logging.info(f"Id of inserted person: {id_person}")
    create_employee(id_person, db)

def create_employee(id, db: DataBase): 
    """
    To add the role of employee to a person who has already created an account in the company 
    
    Args: 
    id : the id of the person that has already had an account in the company 
    db (DataBase): Data base connected for HR 
    """
    db.connect()
    
    print("Now you will give the job of the user with this id")

    salary_person = get_int("Please enter the salary of the person: ")
    description_person = get_string("Please enter the description of the job of the person in the company: ")
    activity = True
   
    db.execute_with_params("INSERT INTO STAFF (id, salary, job_description, active) VALUES (%s,%s,%s, %s)", (id, salary_person, description_person, activity))
    
    print("\n Choose the category of the person: ")
    print("Type 0 if the person is an anaesthetist")
    print("Type 1 if the person is a nurse")
    print("Type 2 if the person is a doctor")
    print("Type 3 if the person is an accountant")
    print("Type 4 if the person is a HR person")
    print("Type 5 if the person is a CEO")
    print("Type 6 if the person does not belong to a particular category")
    
    category = -1
    while category not in {0,1,2,3,4,5,6} :
        category = get_int("The number of the category is: ")
              
    if category == 0:
        inami = get_string("Enter the INAMI number of the person:")
        db.execute_with_params("INSERT INTO ANAESTHESIST (id,inami_number) VALUES (%s, %s)", (id, inami))
    if category == 1: 
        db.execute_with_params("INSERT INTO NURSE (id) VALUES (%s)", (id))
    if category == 2: 
        inami = get_string("Enter the INAMI number of the person:")
        db.execute_with_params("INSERT INTO DOCTOR (id,inami_number) VALUES (%s, %s)", (id, inami))
    if category == 3: 
        db.execute_with_params("INSERT INTO ACCOUNTANT (id) VALUES (%s)", (id))
    if category == 4:  
        db.execute_with_params("INSERT INTO HR (id) VALUES (%s)", (id))
    if category == 5: 
        db.execute_with_params("INSERT INTO CEO (id) VALUES (%s)", (id))
        
    logging.info("Employee well created \n " )
    
    db.disconnect()
            
def modify_employee(db : DataBase): 
    """_
    To modify an actual employee (to change his description or his salary)
    
    Args:
    db (DataBase): Data base connected for HR 
    """
    db.connect()
 
    id_employee = None 
    while id_employee == None: 
        id_employee = get_valid_id(db, "Enter the id of the employee that you want to modify: ", "STAFF")
    
    print("What do you want to do?")
    choice = get_int("Type 1 if you want to modify the salary of the employee and 2 if you want to modify his description:")
    
    if choice == 1: 
        db.execute(f"SELECT salary from STAFF where id= {id_employee}")
        actual_salary = db.table
        print('This is the actual salary of the employee: %s', actual_salary)
        new_salary = get_int("Enter the new salary: ")
        db.execute_with_params("UPDATE STAFF SET salary = %s WHERE id = %s", [new_salary, id_employee]) 
    elif choice == 2: 
        db.execute(f"SELECT job_description from STAFF where id = {id_employee}")
        actual_description = db.table
        print('This is the actual description of the employee: %s', actual_description)
        new_description = get_string("Enter the new description: ")
        db.execute_with_params("UPDATE STAFF SET job_description = %s WHERE id = %s; ", [new_description, id_employee])
    else:
        print("This operation is not possible, please choose another number")
    
    if choice == 1 or choice == 2:
        print("Employee well modified")
    
    db.disconnect()
    
def delete_employee(db: DataBase): 
    """
    To delete an employee (delete his data from STAFF, after that the person has to delete herself her account PERSON)
    
    Args: 
    db (DataBase): Data base connected for HR 
    """
    db.connect()
    
    id_employee = None 
    while id_employee == None: 
        id_employee = get_valid_id(db, "Enter the id of the employee that you want to delete: ", "STAFF")

    id = (id_employee, )
    print("Are you sure to delete this employee? After that you cannot go back ")
    
    confirmation = ""
    while (confirmation != "yes" and confirmation != "no"):
        confirmation = get_string("Type yes if you want to delete this person or no otherwise: ").strip().lower()
    
    if confirmation.startswith('y'):  
        #Verify if the person is in a category
        db.execute("SELECT id FROM DOCTOR")
        medecins = db.table
        doctors = db.table
        db.execute("SELECT id FROM NURSE")
        medecins += db.table 
        db.execute("SELECT id FROM ANAESTHESIST")
        medecins += db.table
        anaesthetists = db.table   
        db.execute("SELECT id FROM CEO")
        ceo = db.table    
        
        if id in medecins:
            if id in doctors:
                db.execute(f"UPDATE DOCTOR SET inami_number = '-1' WHERE id = {id_employee}")
                
            if id in anaesthetists: 
                db.execute(f"UPDATE ANAESTHESIST SET inami_number = '-1' WHERE id = {id_employee}")
            
            db.execute(f"UPDATE STAFF SET salary = '0',job_description = 'nothing', active = false  WHERE id = {id_employee} ")

            logging.debug(f"Id of medecin to delete: {id}")
            print(f"list of medecin id: {medecins}")
        
        if (id not in ceo) and (id not in medecins) :
            db.execute("SELECT id FROM ACCOUNTANT")
            accountants = db.table
            db.execute("SELECT id FROM HR")
            HRpeople = db.table 
            
            if id in accountants: 
                db.execute(f"DELETE FROM ACCOUNTANT WHERE id = {id_employee}")
            if id in HRpeople: 
                db.execute(f"DELETE FROM HR WHERE id = {id_employee}")        
            
            db.execute(f"DELETE FROM STAFF WHERE id = {id_employee} ") 
            
            logging.info(f"Id of employee to delete: {id}")
            logging.info(f"list of employee id: {accountants + HRpeople}")
            
        print('Employee well deleted')
       
    if confirmation.startswith('n'): 
        print('This employee will not be deleted')
        
    db.disconnect()