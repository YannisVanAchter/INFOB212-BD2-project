# encoding uft-8

from module import DataBase, get_int, get_valid_id, get_string


def main_infirmier_menu(database: DataBase):
    """
    Allows a nurse to navigate through their patients, operations, and colleagues based on their requests.
    This function prints the results of the nurse's requests to the database.

    Author: Eline Mota
    """

    print("Nurse menu")
    id = get_int("What is your nurse identifier?")  # Get the nurse's identifier

    while True:
        print("What would you like to do?")
        print("Press 1 to see the people you work with")
        print("Press 2 to see the dates of your future operations")
        print("Press 3 to get information about an organ you will transplant")
        print("Press 4 to get information about a specific client")
        print(
            "Press 5 or any other key to stop requesting information from the database"
        )

        choice = get_int("Choice: ")

        if choice == 1:
            seepeople(database, id)
        elif choice == 2:
            seedate_operations(database, id)
        elif choice == 3:
            info_organe(database)
        elif choice == 4:
            info_client(database)
        else:
            break


def seepeople(database: DataBase, id):
    """
    Allows a nurse to see the people they work with on a specific date of an operation.
    This function prints the IDs of the anesthesiologist and doctor the nurse works with.

    Author: Eline Mota
    """
    database.connect()

    idT = get_int(
        "What is the identifier of the transplantation for which you want to see who you will work with?"
    )

    # Find the anesthesiologists who work with the nurse on the given date and based on the nurse's ID
    anesthesiologist = "SELECT id, inami_number FROM ANESTHESIOLOGIST WHERE id IN (SELECT A_w_id FROM TRANSPLANTATION WHERE id = '%s')"

    database.execute(anesthesiologist % idT)

    print("Here are the people you will work with:")

    for i in database.table:
        print("You work with this anesthesiologist:", i)

    database.disconnect()

    database.connect()

    # Find the doctor who works with the nurse on the given date and based on the nurse's ID
    doctor = "SELECT id FROM DOCTOR WHERE id IN (SELECT D_w_id FROM TRANSPLANTATION WHERE id = '%s')"

    database.execute(doctor % idT)

    for num in database.table:
        print("You work with these doctors:", num)

    database.disconnect()


def seedate_operations(database: DataBase, id):
    """
    According to the id of the nurse, this function allows him to see the futur dates of the transplantation he will have to make
    This function prints the different dates of his futures operations

    Author: Eline Mota

    """
    database.connect()

    dates = "SELECT date_ FROM TRANSPLANTATION WHERE id IN (SELECT id FROM N_work_on WHERE N_N_id = %s)"
    database.execute(dates % (id))

    for date in database.table:
        print("You have operations on these dates:", date)

    database.disconnect()


def info_organe(database: DataBase):
    """
    This function allows a doctor to see the state, the method of preservation, and the type of an organ by printing it

    Author: Eline Mota

    """
    database.connect()

    id_transplantation = int(
        input(
            "Can you provide the identifier of the transplantation for which you want to see the organs?"
        )
    )

    organs = "SELECT state, method_of_preservation, type FROM ORGANE WHERE id = '%s'"
    database.execute(organs % (id_transplantation))

    for state, preservation_method, organ_type in database.table:
        print("Here are the organ's information:")
        print("Organ type:", organ_type)
        print("Organ state:", state)
        print("Preservation method:", preservation_method)

    database.disconnect()


def info_client(database: DataBase):
    """
    This function allows a doctor to see the username, blood type, and blood sign of a patient on whom they will operate.
    This function will print the username, blood type, and blood sign of a given patient based on their ID.

    Authors: Eline Mota

    """
    client = input(
        "What is the ID of the patient for whom you want to retrieve information? "
    )
    database.connect()
    clients = "SELECT Username, blood_type, blood_sign FROM CUSTOMER WHERE id = '%s'"

    database.execute(clients % (client))

    for username, blood_type, blood_sign in database.table:
        print("Here is the information about the patient:")
        print("Username:", username)
        print("Blood Type:", blood_type)
        print("Blood Sign:", blood_sign)
