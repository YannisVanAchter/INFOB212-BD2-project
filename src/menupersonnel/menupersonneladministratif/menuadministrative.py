from module.get import *
from constants import *
from module import *
import logging



def main_persoadmin_menu(db: DataBase):
    """
    Main function of the menu for personnal administratif.

    allow the personnal administratif to:
    -------------------------------------
    - Ask for an organe, check if it is available
    - Ask for a date, check if it is available
    - Associate a doctor, an anesthesist, one or two nurse
    - Calculate the price of the Transplantation
    - Insert into the table TRANPLANTATION

    Args:
        db (DataBase): Data base connected for personnal administratif
        
    Author:
    -------
        Aline Boulanger
    """

    db.connect()

    def print_menu():
        print("Welcome in the administrative menu")

        print("Enter 1 if you want to insert a new transplantation")
        print("Enter 2 if you want to exit ")

    finish = False

    while finish == False:
        print_menu()
        choice = get_int("What is the menu that you need ?")

        if choice == 1:
            customer_id = None
            while customer_id == None:
                customer_id = select_and_print_choice(
                    db,
                    "SELECT C.id, C.pseudo FROM CUSTOMER C",
                    ["id", "pseudo"],
                    "CUSTOMER",
                )

            # Choice of the organe
            db.execute("SELECT O.type FROM ORGANE O WHERE O.id not in (SELECT D.ORGANE FROM DETAIL D WHERE D.ORGANE is not null) AND O.id not in (SELECT T.Con_id FROM TRANSPLANTATION T) GROUP BY O.type;")
            logging.debug(db.table)
            organes_available_list = [i[0] for i in db.table if (i[0] in ORGAN_DICO.keys())]
            logging.debug(organes_available_list)
            print("List of organes available : ", ", ".join(organes_available_list))
            organe_type_choice = get_string(
                "You are there for a transplantation on which organe? "
            )
            if organe_type_choice in ORGAN_DICO:
                print(
                    "Your selection is valid, thank you, we will check if such an organe is available"
                )
                insert_transplantation(db, organe_type_choice, customer_id)

        elif choice == 2:
            finish = True
        else:
            print("Your selection is not valid, please start from the beginning.")


def insert_transplantation(db: DataBase, organe_type_choice, customer_id):
    """
    Menu for personnal administratif.

    allow the personnal administratif to:
    -------------------------------------
    - Ask for an organe, check if it is available
    - Ask for a date, check if it is available
    - Associate a doctor, an anesthesist, one or two nurse
    - Calculate the price of the Transplantation
    - Insert into the table TRANPLANTATION

    Args:
        db (DataBase): Data base connected for personnal administratif
        
    Author:
    -------
        Aline Boulanger
    """

    # Check if such an organe is available and assiciation faire en sous requetes
    db.execute_with_params(
        "SELECT O.id FROM ORGANE O WHERE O.type = %s and O.id not in(SELECT D.id FROM DETAIL D WHERE D.id = O.id) and O.id not in (SELECT T.Con_id FROM TRANSPLANTATION T WHERE T.Con_id = O.id);",
        [organe_type_choice],
    )
    organe_choice = db.tableArgs
    if len(organe_choice) == 0:
        print("All of the organes of the type you have choice is occuped")
    else:
        organe_id = organe_choice[0][0]
        print("Your organe is", organe_id)

    # To get the date of the operation
    if len(organe_choice) != 0:
        while True:
            date_choice = get_date("Enter a date for your operation")
            db.execute("SELECT T.date_ FROM TRANSPLANTATION T;")
            date_table = db.table

            if date_choice is not date_table:
                print("Your operation will attend on", date_choice)
                break

            else:
                print("Your choice is not valid, please start from the beginning idiot")
                continue
    else:
        print("No possibilties for this organes")

    if len(organe_choice) != 0:
        print("We will assign you a doctor, an anaesthetist and a or 2 nurse(s)")

        # To get the doctors who are free
        db.execute_with_params(
            "SELECT D.inami_number, D.id FROM DOCTOR D WHERE D.id not in (SELECT T.D_w_id FROM TRANSPLANTATION T WHERE T.date_ = %s);",
            [date_choice],
        )
        doctor_choice = db.tableArgs  # récupère le résultat de la requête
        if len(doctor_choice) == 0:
            print("All of the medecins is occuped")
        else:
            doc_id = doctor_choice[0][1]  # get the doc inami from the result
            print("Your medecin is ", doctor_choice[0][0])

        # To get the anesthesists who are free
        db.execute_with_params(
            "SELECT A.inami_number, A.id FROM ANAESTHESIST A WHERE A.id not in (SELECT T.A_w_id FROM TRANSPLANTATION T WHERE T.date_ = %s);",
            [date_choice],
        )
        anesthesist_choice = db.tableArgs
        if len(anesthesist_choice) == 0:
            print("All of the anesthesist is occuped")
        else:
            anesthesist_id = anesthesist_choice[0][
                1
            ]  # get the anesthesist inami from the result
            print("Your anesthesist is ", anesthesist_choice[0][0])

        # To get the nurses who are free
        db.execute_with_params(
            "SELECT N.id FROM NURSE N WHERE N.id not in (SELECT NW.N_N_id FROM N_work_on NW WHERE NW.id in (SELECT T.id FROM TRANSPLANTATION T WHERE T.date_ = %s));",
            [date_choice],
        )
        nurse_choice = db.tableArgs
        if len(nurse_choice) == 0:
            print("All of the nurse is occuped")
        else:
            nurse1_id = nurse_choice[0][0]  # get the nurse id from the result
            print("Your nurse is ", nurse1_id)
            nursenbr_choice = get_int(
                "By default, you have one nurse, do you want a second one ? If yes, please, type 1 and 0 if one nurse is enougth for you "
            )
            if nursenbr_choice == 1 and len(nurse_choice) >= 2:
                nurse2_id = nurse_choice[1][0]
                print("Your second nurse is ", nurse2_id)
            elif nurse_choice == 1:
                print("There are no more nurse who is available")

        if (
            len(doctor_choice) != 0
            and len(anesthesist_choice) != 0
            and len(nurse_choice) != 0
        ):
            # To get the salary of the staff
            doctor_salary = SALARY_DOCTOR_TRANSPL[organe_type_choice]
            anesthesist_salary = SALARY_ANESTHESIST_TRANSPL[organe_type_choice]
            if nursenbr_choice == 1:
                nurse_salary = SALARY_NURSE_TRANSPL[organe_type_choice] * 2
            else:
                nurse_salary = SALARY_NURSE_TRANSPL[organe_type_choice]

            salary_total = doctor_salary + anesthesist_salary + nurse_salary

            # To get the price of the transplantation
            transplantation_price = salary_total

            # Check dans BLOOD
            bloodtype_customer = None
            bloodsign_customer = None 
            db.execute(f"SELECT C.blood_type, C.blood_sign FROM CUSTOMER C WHERE C.id = {customer_id}")
            bloodtype_customer = db.table[0][0]
            bloodsign_customer = db.table[0][1]
            logging.debug(bloodsign_customer, type(bloodsign_customer))
            logging.debug(bloodtype_customer, type(bloodtype_customer))


            querry = "SELECT B.id FROM BLOOD B WHERE B.Nee_id is null and B.expiration_date > %s and B.id not in (SELECT D.BLOOD FROM DETAIL D WHERE D.BLOOD is not null)"
            
            querry += " AND B.signe = %s AND ("

            as_previous = False
            if bloodtype_customer in ["AB", "A", "B", "O"]:
                as_previous = True 
                querry += "B.type = 'O'"
            if bloodtype_customer in ["AB", "A"] :
                if as_previous :
                    querry += " OR "
                as_previous = True 
                querry += "B.type = 'A'"
            if bloodtype_customer in ["AB", "B"] :
                if as_previous :
                    querry += " OR "
                as_previous = True 
                querry += "B.type = 'B'"
            if bloodtype_customer in ["AB"] :
                if as_previous :
                    querry += " OR "
                as_previous = True 
                querry += "B.type = 'AB'"
            querry += ");"

            db.execute_with_params(
                querry,
                [date_choice, bloodsign_customer],
            )

            selected_blood = db.tableArgs
            nb_pochesblood_free = ORGAN_DICO[organe_type_choice][1]
            if len(selected_blood) < nb_pochesblood_free:
                print("There are not enough blood bags which are free")
                return

            # Insert in the table TRANSPLANTATION
            id_transplantation = insert_into(
                database=db,
                table="TRANSPLANTATION",
                attributes=("date_", "Con_id", "price", "Rec_id", "D_w_id", "A_w_id"),
                values=(
                    date_choice,
                    organe_id,
                    transplantation_price,
                    customer_id,
                    doc_id,
                    anesthesist_id,
                ),
            )

            # Insert in the table BLOOD
            for bag_id in range(nb_pochesblood_free):
                logging.debug(selected_blood)
                blood_id = selected_blood[bag_id][0]  # to get the id of the blood bag
                logging.debug(id_transplantation)
                logging.debug(blood_id)
                logging.debug(type(id_transplantation))
                logging.debug(type(blood_id))
                db.execute(
                    "UPDATE BLOOD B SET B.Nee_id = %s WHERE B.id = %s;" %
                    (id_transplantation, blood_id)
                )
            print(
                "Your transplantation is inserted with success, thank you for your visit <3"
            )

        else:
            print(
                "Unfortunately, nobody is available for your transplantation so comme back later"
            )

