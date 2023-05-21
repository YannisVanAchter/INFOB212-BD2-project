# encoding uft-8

from datetime import date
import logging

from module import DataBase, get_int, get_string, select_and_print_choice, print_table, print_selection
from auth import User


def main_infirmier_menu(database: DataBase, user: User):
    """
    Allows a nurse to navigate through their patients, operations, and colleagues based on their requests.
    This function prints the results of the nurse's requests to the database.

    Author: Eline Mota
    """

    print("Nurse menu")
    id = user.id  # Get the nurse's identifier
    if "CEO" in user.userGroup:
        other = True
        if "NURSE" in user.userGroup:
            other = get_string("Do you want to connect to another nurse? (y/n)").lower().strip().startswith("y")
        
        if other:
            print("Select the medecin you want to connect:")
            id = select_and_print_choice(
                database,
                "SELECT P.id, P.last_name, P.first_name, P.email, P.phone_number FROM PERSON P, STAFF S WHERE P.id = S.id AND S.active = True AND P.id IN (SELECT id FROM NURSE)",
                [" ID ", "   Last name   ", "   First name   ", "          Email          ", "     Phone number     "],
                "NURSE"
            )
               

    while True:
        print("What would you like to do?")
        print("Press 1 to see the people you work with")
        print("Press 2 to see the dates of your future operations")
        print("Press 3 to get information about an organ you will transplant")
        print("Press 4 to get information about a specific client")
        print(
            "Press 5 or any other key to stop requesting information from the database"
        )

        choice = get_string("Choice: ").strip()

        if choice == "1":
            seepeople(database, id)
        elif choice == "2":
            seedate_operations(database, id)
        elif choice == "3":
            info_organe(database, id)
        elif choice == "4":
            info_client(database, id)
        else:
            break


def seepeople(database: DataBase, id):
    """
    Allows a nurse to see the people they work with on a specific date of an operation.
    This function prints the IDs of the anesthesiologist and doctor the nurse works with.

    Author: Eline Mota
    """
    database.connect()
    
    print("Here are the ids of your future transplantations, select one you want to see informations about")
    idT = select_and_print_choice(
        database,
        f"SELECT id, client, type_blood, signe_blood, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND id in (SELECT id FROM N_work_on WHERE N_N_id = {id})",
        [" ID ", "  Customers pseudo  ", "Customer blood type", "Customer blood singe", "   Date   "],
        "TRANSPLANTATION"
    )
    
    print("Anesthesiologists: ")
    print_selection(
        database,
        f"SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (SELECT A_w_id from TRANSPLANTATION WHERE id = {idT})",
        ["   Last name   ", "   First name   ", "          Email          ", "     Phone number     "],
    )
    
    print("Here are the doctors you will be working with:")
    print_selection(
        database,
        f"SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (SELECT D_w_id from TRANSPLANTATION WHERE id = {idT})",
        ["    Last name    ", "    First name    ", "        Email        ", "    Phone number    "]
    )


def seedate_operations(database: DataBase, id):
    """
    According to the id of the nurse, this function allows him to see the futur dates of the transplantation he will have to make
    This function prints the different dates of his futures operations

    Author: Eline Mota
    """
    print_selection(
        database,
        f"SELECT id, client, type_blood, signe_blood, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND id in (SELECT id FROM N_work_on WHERE  N_N_id = {id})",
        ["  id  ", "    Client    ", "Blood type", "Blood signe", "    Date    "]
    )


def info_organe(database: DataBase, id):
    """
    This function allows a doctor to see the state, the method of preservation, and the type of an organ by printing it

    Author: Eline Mota

    """
    print("Enter the id of organe you want information about")
    id_organe = select_and_print_choice(
        database,
        f"SELECT id, client, organe, organe_id, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND id in (SELECT id FROM N_work_on WHERE N_N_id = {id})",
        ["  ID  ", "    Client    ", "    Organe type    ", "Organe ID", "    Date    "],
        "ORGANE",
    )
    
    print_selection(
        database,
        f"SELECT state, method_of_preservation, type FROM ORGANE WHERE id = {id_organe}",
        ["    State    ", "        Method of preservation        ", "        Type        "]
    )


def info_client(database: DataBase, id):
    """
    This function allows a doctor to see the username, blood type, and blood sign of a patient on whom they will operate.
    This function will print the username, blood type, and blood sign of a given patient based on their ID.

    Authors: Eline Mota

    """
    print("Enter the id of client you want information about.")
    client = select_and_print_choice(
        database,
        f"SELECT client, customer_id, organe FROM MEDECIN WHERE date_ >= '{date.today()}' AND id in (SELECT id FROM N_work_on WHERE N_N_id = {id})",
        ["    Client    ", "ID Client", "    Organe    "],
        "ORGANE"
    )
    
    print_selection(
        database,
        f"SELECT pseudo, blood_type, blood_sign FROM CUSTOMER WHERE id = {client}",
        ["  Pseudo  ", "Blood type", "Blood sign"]
    )
    
