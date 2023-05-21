import logging

from module import DataBase, get_int, get_valid_id, get_string
from auth import User


def main_anesthesiologist_menu(database: DataBase, user: User):
    """
    Allows a doctor to navigate through their patients, operations, and colleagues based on their requests.
    This function prints the results of the doctor's requests after querying the Database.

    Author: Eline Mota
    """

    print("In the anesthesiologist menu")
    id = user.id

    while True:
        print("What would you like to do?")
        print("Type 1 if you want to see the people you work with.")
        print("Type 2 if you want to see the dates of your future operations.")
        print(
            "Type 3 if you want information about an organ you are going to transplant."
        )
        print("Type 4 if you want information about a specific client.")
        print(
            "Type 5 or anything else if you want to stop requesting information from the database."
        )

        numero = get_int("Choice:")

        if numero == 1:
            seepeople(database, id)

        elif numero == 2:
            seedate_operations(database, id)

        elif numero == 3:
            info_organe(database)

        elif numero == 4:
            info_client(database)
        else:
            break


def seepeople(database: DataBase):
    """
    Allows an anesthesiologist to see the people they work with based on a specific date of an operation.
    This function prints the ID of the doctor and nurses they work with on a certain date.

    Author: Eline Mota
    """
    database.connect()
    
    #print("Here are the ids of your future transplantations, select one you want to see informations about")
    
    #qq = "Select id FROM TRANSPLANTATION WHERE D_w_id = %s"
    #database.execute_with_params(qq, [id])
    #for idd in database.tableArgs:
        #print("Here are the different id you can select")

    idT = get_valid_id(
        db=database,
        prompt="What is the ID of the transplantation for which you want to see who you will be working with?",
        table_name="TRANSPLANTATION"
    )

    # Find the doctors who work with the anesthesiologist on the given date and according to the doctor's ID
    doctors_query = "SELECT id FROM DOCTOR WHERE id IN (SELECT D_w_id from TRANSPLANTATION WHERE id = %s)"
    #doctors_query = "SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (select id FROM STAFF WHERE id IN (SELECT id FROM DOCTOR WHERE id IN (SELECT D_w_id from TRANSPLANTATION WHERE id = %s)))"
    

    database.execute_with_params(doctors_query, [idT])

    print("Here are the people you will be working with:")

    for i in database.tableArgs:
        print("You work with this doctor:", i)
    database.disconnect()

    database.connect()

    # Find the nurses who work with the anesthesiologist on the given date and according to the doctor's ID
    nurses_query = "SELECT N_N_id FROM N_work_on WHERE id IN (SELECT id FROM TRANSPLANTATION where id = %s)"
    #nurse_query = "SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (select id FROM STAFF WHERE id IN (SELECT id FROM NURSE WHERE id IN (SELECT N_N_id FROM N_work_on WHERE id IN (SELECT id FROM TRANSPLANTATION where id = %s))))"

    database.execute_with_params(nurses_query, [idT])

    for num in database.tableArgs:
        print("You work with these nurses:", num)

    database.disconnect()


def seedate_operations(database: DataBase, id):
    """
    This function allows an anesthesiologist to see the future dates of the transplantations they will have to perform based on their ID.
    This function prints the different dates of their future operations.

    Author: Eline Mota

    """
    database.connect()

    dates_query = "SELECT date_ FROM TRANSPLANTATION WHERE A_w_id = %s"
    database.execute_with_params(dates_query, [id])

    for date in database.tableArgs:
        print("You have operations on these dates:", date)

    database.disconnect()


def info_organe(database: DataBase):
    """
    This function allows a doctor to see the state, preservation method, and type of an organ by printing it.

    Author: Eline Mota

    """
    database.connect()

    id_transplantation = get_valid_id(
        db=database,
        prompt="Can you provide me with the ID of the transplantation for which you want to see the organs?",
        table_name="TRANSPLANTATION"
    )

    organs_query = (
        "SELECT state, method_of_preservation, type FROM ORGANE WHERE id = %s"
    )
    database.execute_with_params(organs_query, [id_transplantation])

    for state, preservation_method, organ_type in database.tableArgs:
        print("Here is the information about the organ:")
        print("Type of organ to be transplanted:", organ_type)
        print("State of this organ:", state)
        print("Method of preservation for this organ:", preservation_method)

    database.disconnect()


def info_client(database: DataBase):
    """
    This function allows a doctor to see the username, blood type, and blood sign of a patient on whom they will have to operate.
    This function will print the username, blood type, and blood sign of a given patient based on their ID.

    Authors: Eline Mota

    """
    client = get_valid_id(
        db=database,
        prompt="What is the ID of the patient for whom you want to get the information? ",
        table_name="CUSTOMER"
    )
    database.connect()
    clients_query = (
        "SELECT pseudo, blood_type, blood_sign FROM CUSTOMER WHERE id = %s"
    )

    database.execute_with_params(clients_query, [client])

    for Username, blood_type, blood_sign in database.tableArgs:
        print("Here is the information about the client:")
        print("Username:", Username)
        print("Blood type:", blood_type)
        print("Blood sign:", blood_sign)
