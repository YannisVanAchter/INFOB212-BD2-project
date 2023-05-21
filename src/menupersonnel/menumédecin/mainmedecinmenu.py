# encoding utf-8

from datetime import date
import logging

from module import DataBase, get_int, get_string, select_and_print_choice, print_table, print_selection
from auth import User


def main_medecin_menu(database: DataBase, user: User):
    """
    Allows a medecin to navigate throughout his patients, his operations and his colleguas according to what he asks
    This function prints what the medecin has aksed for after making requests to the Database

    Author: Eline Mota
    """

    logging.info("In médecin menu")
    id = user.id
    if "CEO" in user.userGroup:
        connect_other = True
        if "MEDECIN" in user.userGroup:
            connect_other = get_string("Do you want to connect to another medecin? (y/n)").lower().strip().startswith("y")
        
        if connect_other:
            print("Select the medecin you want to connect:")
            id = select_and_print_choice(
                database,
                "SELECT P.id, P.last_name, P.first_name, P.email, P.phone_number FROM PERSON P, STAFF S WHERE P.id = S.id AND S.active = True AND P.id IN (SELECT id FROM DOCTOR)",
                [" ID ", "   Last name   ", "   First name   ", "          Email          ", "     Phone number     "],
                "DOCTOR"
            )

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

        numero = get_string("Choice: ").strip()

        if numero == "1":
            seepeople(database, id)

        elif numero == "2":
            seedate_operations(database, id)

        elif numero == "3":
            info_organe(database, id)

        elif numero == "4":
            info_client(database, id)
        else:
            break


def seepeople(database: DataBase, id):
    """
    Allows a doctor to see the people they work with according to the date of an operation.
    This function prints the ID and INAMI number of the anesthesiologist and nurses they work with on a certain date.

    Author: Eline Mota
    """
    database.connect()
    
    print("Here are the ids of your future transplantations, select one you want to see informations about")
    
    idT = select_and_print_choice(
        database,
        f"SELECT id, client, type_blood, signe_blood, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND medecin_id = {id}",
        [" ID ", "  Customers pseudo  ", "Customer blood type", "Customer blood singe", "   Date   "],
        "TRANSPLANTATION"
    )

    # Find anesthesiologists who work with the doctor on the given date and according to the doctor's ID
    print("Anesthesiologists: ")
    print_selection(
        database,
        f"SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (SELECT A_w_id from TRANSPLANTATION WHERE id = {idT})",
        ["   Last name   ", "   First name   ", "          Email          ", "     Phone number     "],
    )
    database.disconnect()

    database.connect()

    # Find nurses who work with the doctor on the given date and according to the doctor's ID

    print("Nurses: ")
    print_selection(
        database,
        f"SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (SELECT N_N_id FROM N_work_on WHERE id IN (SELECT id FROM TRANSPLANTATION where id = {idT}))",
        ["   Last name   ", "   First name   ", "          Email          ", "     Phone number     "],
    )
    database.disconnect()


def seedate_operations(database: DataBase, id):
    """
    According to the id of the medecin, this function allows him to see the futur dates of the transplantation he will have to make
    This function prints the different dates of his futures operations

    Author: Eline Mota

    """
    database.connect()

    print_selection(
        database,
        f"SELECT id, client, type_blood, signe_blood, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND medecin_id = {id}",
        [" ID ", "  Customers pseudo  ", "Customer blood type", "Customer blood singe", "     Date     "],
    )

    database.disconnect()


def info_organe(database: DataBase, id):
    """
    This function allows a doctor to see the state, preservation method, and type of an organ by printing it.

    Author: Eline Mota

    """
    database.connect()
    
    print("Here are the ids of your future transplantations, select one you want to see informations about the organ you're going to tranplant")
    
    id_transplantation = select_and_print_choice(
        database,
        f"SELECT organe, organe_id, client, type_blood, signe_blood, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND medecin_id = {id}",
        ["      Organe type      ", " ID ", "  Customers pseudo  ", "Customer blood type", "Customer blood singe", "     Date     "],
        "ORGANE"
    )

    organ_query = (
        "SELECT state, method_of_preservation, type FROM ORGANE WHERE id = %s"
    )
    database.execute(organ_query % (id_transplantation))

    print("Here is the information about the organ:")
    print_table(
        database.table,
        ["   State   ", "            Method of preservation            ", "      Type      "],
    )

    database.disconnect()


def info_client(database: DataBase, id):
    """
    This function allows a doctor to see the username, blood type, and blood sign of a patient on whom they will have to operate.
    This function will print the username, blood type, and blood sign of a given patient according to their ID.

    Authors: Eline Mota

    """
    client = select_and_print_choice(
        database,
        f"SELECT  client, customer_id, organe FROM MEDECIN WHERE date_ >= '{date.today()}' AND medecin_id = {id}",
        ["  Pseudo  ", " ID ", "      Organe type      "],
        "CUSTOMER"
    )
    
    print_selection(
        database,
        f"SELECT pseudo, blood_type, blood_sign FROM CUSTOMER WHERE id = {client}",
        ["  Pseudo  ", "Blood type", "Blood sign"]
    )
