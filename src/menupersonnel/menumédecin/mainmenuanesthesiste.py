
from datetime import date

from module import DataBase, get_int, get_string, select_and_print_choice, print_table, print_selection
from auth import User


def main_anesthesiologist_menu(database: DataBase, user: User):
    """
    Allows a doctor to navigate through their patients, operations, and colleagues based on their requests.
    This function prints the results of the doctor's requests after querying the Database.

    Author: Eline Mota
    """

    print("In the anesthesiologist menu")
    id = user.id
    if "CEO" in user.userGroup:
        other = True
        if "ANAESTHESIST" in user.userGroup:
            other = get_string("Do you want to see someone else's information? (Y/N)").upper().strip() == "Y"
        if other:
            print("Select the anesthesiologist you want to see:")
            id = select_and_print_choice(
                database,
                "SELECT P.id, P.last_name, P.first_name, P.email, P.phone_number FROM PERSON P, STAFF S WHERE P.id = S.id AND S.active = True AND P.id IN (SELECT id FROM ANAESTHESIST)",
                [" ID ", "   Last name   ", "   First name   ", "          Email          ", "     Phone number     "],
                "ANAESTHESIST"
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
    Allows an anesthesiologist to see the people they work with based on a specific date of an operation.
    This function prints the ID of the doctor and nurses they work with on a certain date.

    Author: Eline Mota
    """
    database.connect()
    
    print("Here are the ids of your future transplantations, select one you want to see informations about")
    idT = select_and_print_choice(
        database,
        f"SELECT id, client, type_blood, signe_blood, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND anesthesiste_id = {id}",
        [" ID ", "  Customers pseudo  ", "Customer blood type", "Customer blood singe", "   Date   "],
        "TRANSPLANTATION"
    )

    # Find the doctors who work with the anesthesiologist on the given date and according to the doctor's ID
    print("Here are the doctors you will be working with:")
    print_selection(
        database,
        f"SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (SELECT D_w_id from TRANSPLANTATION WHERE id = {idT})",
        ["    Last name    ", "    First name    ", "        Email        ", "    Phone number    "]
    )
    
    # Find the nurses who work with the anesthesiologist on the given date and according to the doctor's ID
    print("Here are the nurses you will be working with:")    
    print_selection(
        database,
        f"SELECT last_name, first_name, email, phone_number FROM PERSON WHERE id IN (SELECT N_N_id FROM N_work_on WHERE id IN (SELECT id FROM TRANSPLANTATION where id = {idT}))",
        ["    Last name    ", "    First name    ", "        Email        ", "    Phone number    "]
    )


def seedate_operations(database: DataBase, id):
    """
    This function allows an anesthesiologist to see the future dates of the transplantations they will have to perform based on their ID.
    This function prints the different dates of their future operations.

    Author: Eline Mota

    """
    print_selection(
        database,
        f"SELECT id, client, type_blood, signe_blood, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND anesthesiste_id = {id}",
        ["  id  ", "    Client    ", "Blood type", "Blood signe", "    Date    "]
    )


def info_organe(database: DataBase, id):
    """
    This function allows a doctor to see the state, preservation method, and type of an organ by printing it.

    Author: Eline Mota

    """
    print("Enter the id of organe you want information about")
    id_organe = select_and_print_choice(
        database,
        f"SELECT id, client, organe, organe_id, date_ FROM MEDECIN WHERE date_ >= '{date.today()}' AND anesthesiste_id = {id}",
        ["  ID  ", "    Client    ", "    Organe type    ", "Organe ID", "    Date    "],
        "ORGANE",
    )
    
    print_selection(
        database,
        f"SELECT state, method_of_preservation, type FROM ORGANE WHERE id = {id_organe}",
        ["    State    ", "        Method of preservation        ", "    Type    "]
    )


def info_client(database: DataBase, id):
    """
    This function allows a doctor to see the username, blood type, and blood sign of a patient on whom they will have to operate.
    This function will print the username, blood type, and blood sign of a given patient based on their ID.

    Authors: Eline Mota

    """
    print("Enter the id of client you want information about.")
    client = select_and_print_choice(
        database,
        f"SELECT client, customer_id, organe FROM MEDECIN WHERE date_ >= {date.today()} AND anesthesiste_id = {id}",
        ["    Client    ", "ID Client", "    Organe    "],
        "ORGANE"
    )
    
    print_selection(
        database,
        f"SELECT pseudo, blood_type, blood_sign FROM CUSTOMER WHERE id = {client}",
        ["  Pseudo  ", "Blood type", "Blood sign"]
    )
    
