from module.get import *
from constants import *
from module.utils import *
from menuconnexion.menu import *
from menupersonnel.menuaccounting.mainaccountingmenu import main_accounting_menu, insert_organ
from menupersonnel.menumédecin.mainmedecinmenu import main_medecin_menu
from menupersonnel.menumédecin.mainmenuanesthesiste import main_anesthesiologist_menu
from menupersonnel.menumédecin.menuinfirmier import main_infirmier_menu
from menupersonnel.menupersonneladministratif import main_persoadmin_menu
from menupersonnel.RH import main_RH_menu
from module.database import DataBase


def main_PDG_menu(database: DataBase, user_id):
    """
    Main function of the menu for the PDG.

    allow the PDG to:
    -------------------------------------
    - to naviguate in the differents menus
    - to go to the function insert_newelements
    - to go to the function suppression_PDG

    Args:
        db (DataBase): Data base connected for personnal administratif
        user_id : the id of the CEO that we want to delete and which is connected

    Author:
    -------
        Louise Delpierre
    """

    def print_menu():
        print("Welcome in the PDG menu")

        print("Enter 1 if you want to access to the accounting menu")
        print("Enter 2 if you want to access to the medecin menu")
        print("Enter 3 if you want to access to the anesthetist menu")
        print("Enter 4 if you want to access to the nurse menu")
        print("Enter 5 if you want to access to the administratif menu")
        print("Enter 6 if you want to access to the RH menu")
        print("Enter 7 if you want to access to the functions of the PDG menu")
        print("Enter 8 if you want to exit ")

    finish = False

    while finish == False:
        print_menu()
        menu_choice = get_int("What is the menu that you need ?")
        if menu_choice not in {1, 2, 3, 4, 5, 6, 7, 8}:
            print("This operation is not possible, please choose another number")

        else:
            database.connect()

            if menu_choice == 1:
                main_accounting_menu(database)
            elif menu_choice == 2:
                main_medecin_menu(database)
            elif menu_choice == 3:
                main_anesthesiologist_menu(database)
            elif menu_choice == 4:
                main_infirmier_menu(database)
            elif menu_choice == 5:
                main_persoadmin_menu(database)
            elif menu_choice == 6:
                main_RH_menu(database)
            elif menu_choice == 7:
                print(
                    "Enter 1 if you want to access to the function which allows to delete a PDG"
                )
                print(
                    "Enter 2 if you want to access to the function which allows to insert something in the DataBase"
                )
                function_choice = get_int("What is your choice ?")

                if function_choice == 1:
                    suppression_PDG(database, user_id)
                elif function_choice == 2:
                    insert_newelements(database)
                else:
                    print("The number entered is not valid")

            elif menu_choice == 8:
                finish = True


def suppression_PDG(db: DataBase, user_id):
    """
    Menu to delete a PDG.

    allow the PDG to:
    -------------------------------------
    - allow to delete a CEO of the DB

    Args:
        db (DataBase): Data base connected for personnal administratif
        user_id : the id of the CEO that we want to delete and which is connected

    Author:
    -------
        Louise Delpierre
    """
    db.connect()

    db.execute_with_params("DELETE FROM CEO C, STAFF S WHERE C.id = %s", [user_id])


def insert_newelements(db: DataBase):
    """
    Menu to insert a new element in DB.

    allow the PDG to:
    -------------------------------------
    - allow to insert a new element in the DB.

    Args:
        db (DataBase): Data base connected for personnal administratif

    Author:
    -------
        Louise Delpierre
    """
    db.connect()

    # Insert a new organ
    print("Do you want to add an organ?")
    organ = get_string("Yes or No ?").lower().strip()
    if organ.startswith("n"):
        return
    organ_new = get_string("Which one ?")
    organ_new_price = get_float("What is the price of your new organ ?")
    organ_500ML = get_int(
        "How much blood bag of 500 ml do we need for a transplantation of this new organ ? (It could be 0) "
    )

    if organ_new not in ORGAN_DICO:
        ORGAN_DICO.update({organ_new: [organ_new_price, organ_500ML]})
        insert_organ()
    else:
        print("This type of organ already exist ;)")

    # Insert a new type of delivery
    print("Do you want to add a new type of delivery ?")
    tp_delivery = get_string("Yes or No ?")
    tp_delivery_id = get_string("Which one ?")
    tp_delivery_new_price = get_float("What is its price ?")
    if tp_delivery == "Yes":
        insert_into(
            database=db,
            table="TYPE_DELIVERY",
            attributes=("id", "price"),
            values=(tp_delivery_id, tp_delivery_new_price),
        )

    else:
        return 0
