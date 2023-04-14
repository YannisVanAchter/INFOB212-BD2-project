# encoding uft-8

from module.get import get_string, get_float, get_int, get_sql_user_querry
from module.database import DataBase, ProgrammingError
from module.utils import clear_terminal as cls

from .view import ask_product_price, ask_product_type, ask_product_id
from .controler import set_product_price


def case_other():
    print("You did not enter a correct choice")
    print("Please try again")

def update_blood(database: DataBase):
    """Update blood price for a specific blood"""
    print("You are only allow to update price of product (you are currently updating blood)")
    
    product_id = ask_product_id()
    new_blood_price = ask_product_price()
    
    set_product_price(database, new_blood_price, product_id, "BLOOD")

def update_organe(database: DataBase):
    """Update organe price for a specific organe"""
    print("You are only allow to update price of product (you are currently updating ORGANE)")
    
    product_id = ask_product_id()
    new_organe_price = ask_product_price()
    
    set_product_price(database, new_organe_price, product_id, "ORGANE")

def update_type_delivery(database: DataBase):
    """Update type delivery price for a specific type delivery"""
    print("You are only allow to update price of product (you are currently updating TYPE_DELIVERY)")
    
    # on TYPE_DELIVERY the id is a string
    product_id = "b" * 17
    while not (0 < len(product_id) < 16 ):
        product_id = get_string("Enter the type of delivery: ")
        
    new_type_delivery_price = ask_product_price()
    
    set_product_price(database, new_type_delivery_price, product_id, "TYPE_DELIVERY")

def update_menu(database):
    """Menu to update the product price (price because this is the only that can be update by accuntant)"""
    def print_menu():
        print("What do you want to update ?")
        print("1: BLOOD\n2: ORGANE\n3: TYPE_DELIVERY (allow insert)")

    while True:
        print_menu()
        choice = get_string().strip().lower()

        match choice:
            case "1":
                update_blood(database)
                break
            case "2":
                update_organe(database)
                break
            case "3":
                update_type_delivery(database)
                break
            case _:
                case_other()


def insert_blood(database):
    pass


def insert_organ(database):
    pass


def insert_menu(database):
    while True:
        table = get_string("Insert of 'BLOOD' or 'ORGANE': ").strip().upper()

        match table:
            case "BLOOD":
                insert_blood(database)
                return
            case "ORGANE":
                insert_organ(database)
                return
            case other:
                case_other()


def select_selling_quantity(database):
    pass


def select_product_not_sell(database: DataBase):
    """print product that are not sell

    Print organe and blood that are not sell

    Args:
    -----
        database (DataBase): database object connected for this user
    """
    # organe selection
    print(f"Here is the organe that are not sell:")
    select_organe_querry = "SELECT * FROM ORGANE WHERE ORGANE.id NOT IN (SELECT DETAIL.ORGANE FROM DETAIL) AND ORGANE.id NOT IN (SELECT TRANSPLANTATION.Con_id FROM TRANSPLANTATION);"
    with database as db:
        db.execute(select_organe_querry)

        for row in db.table:
            print(row)

    print("\n================================\n")
    # blood selection
    print("Here is the blood that are not sell:")
    select_blood_querry = "SELECT * FROM BLOOD WHERE BLOOD.id NOT IN (SELECT DETAIL.BLOOD FROM DETAIL) AND BLOOD.Nee_id IS NULL;"
    with database as db:
        db.execute(select_blood_querry)

        for row in db.table:
            print(row)


def find_where_are_the_clients(database):
    pass


def get_selling_price_of_each_command(database):
    pass


def resarch_menu(database: DataBase):
    """Allow user to do research for accounting stuff

    Args:
    -----
        database (DataBase): database object connected for this user

    """

    def print_menu():
        print("What do you want to do search ?")
        print("1: Selling quantity")
        print("2: Product quantity (not selling)")
        print("3: where are the clients")
        print("4: get selling price of each command/client")

    while True:
        print_menu()
        search = get_string("Enter you choice: ").strip()

        match search:
            case "1":
                select_selling_quantity(database)
                return
            case "2":
                select_product_not_sell(database)
                return
            case "3":
                find_where_are_the_clients(database)
                return
            case "4":
                get_selling_price_of_each_command(database)
                return
            case other:
                case_other()


def personnal_querry(database: DataBase):
    """Allow user to do a personnal querry

    Args:
    -----
        database (DataBase): database object connected for this user
    """
    while True:
        querry = get_sql_user_querry("Enter your querry:\n")
        try:
            with database as db:
                db.execute(querry)

                if querry.lower().startswith("select"):
                    show_result = (
                        get_string("Do you want to see the result ? (y/n): ")
                        .strip()
                        .lower()
                    )

                    if show_result.startswith("y"):
                        for row in db.table:
                            print(row)

            return None  # exit the loop/function

        except ProgrammingError:
            print("Syntax error in your querry")


def main_accounting_menu(database: DataBase) -> (int):
    """Accountent menu

    allow user to:
    --------------
        - set product price
        - update price
        - insert new product
        - research for accounting stuff
            - selling quantity
            - where are the clients
            - get price of each command
            - get/set price of delivery

    Args:
    -----
        database (DataBase): Data base connected for this user (the accountent)

    Return:
    -------
        int: 0 for normal exit status and 1 for exit program (ctrl + c)
    """

    def print_menu():
        print("You are in the accounting menu")
        print("Type the number of the action you want to do")
        print("1: Update a existing product")
        print("2: Insert a new product")
        print("3: Research for accounting stuff")
        print("4: personnal querry (sql)")
        print("5: Exit")

    while True:
        try:
            print_menu()
            choice = get_string("Enter you choice: ").strip()

            match choice:
                case "1":
                    update_menu(database)
                    break
                case "2":
                    insert_menu(database)
                    break
                case "3":
                    resarch_menu(database)
                    break
                case "4":
                    personnal_querry(database)
                    break
                case "5":
                    cls()
                    return 0
                case other:
                    case_other()

        except KeyboardInterrupt:
            cls()
            return 1
