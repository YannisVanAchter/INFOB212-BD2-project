# encoding utf-8

import logging

from module import DataBase, get_int, get_valid_id
from auth import User


def main_medecin_menu(database: DataBase, user: User):
    """
    Allows a medecin to navigate throughout his patients, his operations and his colleguas according to what he asks
    This function prints what the medecin has aksed for after making requests to the Database

    Author: Eline Mota
    """

    logging.info("In médecin menu")
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

        numero = get_int("Choice: ")

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


def seepeople(database: DataBase, id):
    """
    Allows a doctor to see the people they work with according to the date of an operation.
    This function prints the ID and INAMI number of the anesthesiologist and nurses they work with on a certain date.

    Author: Eline Mota
    """
    database.connect()
    
    #print("Here are the ids of your future transplantations, select one you want to see informations about")
    
    #qq = "Select id FROM TRANSPLANTATION WHERE D_w_id = %s"
    #database.execute_with_params(qq, [id])
    #for idd in database.tableArgs:
        #print("Here are the different id you can select")

    idT = get_int(
        "What is the ID of the transplantation for which you want to see who you will be working with?"
    )

    # Find anesthesiologists who work with the doctor on the given date and according to the doctor's ID
    
    #anesthesiologist_query = "SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (select id FROM STAFF WHERE id IN (SELECT id FROM ANAESTHESIST WHERE id IN (SELECT A_w_id from TRANSPLANTATION WHERE id = %s)))"
    anesthesiologist_query = "SELECT id, inami_number FROM ANAESTHESIST WHERE id IN (SELECT A_w_id from TRANSPLANTATION WHERE id = %s)"
    database.execute_with_params(anesthesiologist_query, [idT])

    print("Here are the people you will be working with:")

    for ana, ina in database.tableArgs:
        print(
            "You will work with this anesthesiologist:",
            ana,
            "who has an INAMI code of",
            ina,
        )
    database.disconnect()

    database.connect()

    # Find nurses who work with the doctor on the given date and according to the doctor's ID
    nurse_query = "SELECT N_N_id FROM N_work_on WHERE id IN (SELECT id FROM TRANSPLANTATION where id = %s)"
    #nurse_query = "SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (select id FROM STAFF WHERE id IN (SELECT id FROM NURSE WHERE id IN (SELECT N_N_id FROM N_work_on WHERE id IN (SELECT id FROM TRANSPLANTATION where id = %s))))"
    
    

    database.execute_with_params(nurse_query, [idT])

    for num in database.tableArgs:
        print("You will work with these nurses:", num)

    database.disconnect()


def seedate_operations(database: DataBase, id):
    """
    According to the id of the medecin, this function allows him to see the futur dates of the transplantation he will have to make
    This function prints the different dates of his futures operations

    Author: Eline Mota

    """
    database.connect()

    dates = "SELECT date_ FROM TRANSPLANTATION WHERE D_w_id = %s"
    database.execute_with_params(dates, [id])

    for date in database.tableArgs:
        print("You have an operation at those dates: ", date)

    database.disconnect()


def info_organe(database: DataBase):
    """
    This function allows a doctor to see the state, preservation method, and type of an organ by printing it.

    Author: Eline Mota

    """
    database.connect()
    
    #print("Here are the ids of your future transplantations, select one you want to see informations about the organ you're going to tranplant")
    
    #qq = "Select id FROM TRANSPLANTATION WHERE D_w_id = %s"
    #database.execute_with_params(qq, [id])
    #for idd in database.tableArgs:
        #print("Here are the different id you can select")

    id_transplantation = get_valid_id(
        database,
        "Can you provide the ID of the transplantation for which you want to see the organs?",
        "ORGANE",
    )

    organ_query = (
        "SELECT state, method_of_preservation, type FROM ORGANE WHERE id = %s"
    )
    database.execute(organ_query % (id_transplantation))

    for state, preservation_method, organ_type in database.table:
        print("Here is the information about the organ:")
        print("Organ type for transplantation:", organ_type)
        print("State of the organ:", state)
        print("Preservation method for this organ:", preservation_method)
        print("*" * 50)

    database.disconnect()


def info_client(database: DataBase):
    """
    This function allows a doctor to see the username, blood type, and blood sign of a patient on whom they will have to operate.
    This function will print the username, blood type, and blood sign of a given patient according to their ID.

    Authors: Eline Mota

    """
    client = get_valid_id(
        database,
        "What is the ID of the client for whom you want to retrieve information? ",
        "CUSTOMER",
    )
    database.connect()
    clients = "SELECT pseudo, blood_type, blood_sign FROM CUSTOMER WHERE id = %s"

    database.execute(clients % (client))

    for Username, blood_type, blood_sign in database.table:
        print("Here is the information about the client:")
        print("Username:", Username)
        print("Blood type:", blood_type)
        print("Blood sign:", blood_sign)
