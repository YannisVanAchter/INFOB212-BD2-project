# encoding uft-8

from datetime import date as Date
import logging
import time

from module.get import get_string, get_sql_user_querry, get_date
from module.database import DataBase, ProgrammingError
from module.utils import clear_terminal as cls, insert_into
from constants import BLOOD_PRICE_FACTOR, ORGAN_DICO

from .view import *
from .controler import *


def main_accounting_menu(database: DataBase) -> (int):
    """Accounting menu

    allows user to:
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
        database (DataBase): Data base connected for this user (the accountant)

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
        print("4: Exit")

    while True:
        cls()
        try:
            print_menu()
            choice = get_string("Enter your choice: ").strip()

            match choice:
                case "1":
                    update_menu(database)
                    continue
                case "2":
                    insert_menu(database)
                    continue
                case "3":
                    resarch_menu(database)
                    continue
                case "4":
                    cls()
                    return 0
                case _:
                    case_other()

        except KeyboardInterrupt:
            cls()
            return 1
        time.sleep(1)


def case_other():
    """Print error message when user did not enter correct option."""
    print("You did not enter a correct choice")
    print("Please try again")
    time.sleep(1)
    

def update_menu(database):
    """Menu to update the product price 
    (price because this is the only thing that can be update by accuntant)
    """

    def print_menu():
        print("What do you want to update ?")
        print("1: BLOOD\n2: ORGANE\n3: TYPE_DELIVERY (allow insert)\n4: EXIT")

    while True:
        print_menu()
        choice = get_string().strip().lower()

        match choice:
            case "1":
                update_blood(database)
                return
            case "2":
                update_organe(database)
                return
            case "3":
                update_type_delivery(database)
                return
            case "4":
                return
            case _:
                case_other()


def update_blood(database: DataBase):
    """Update blood price for a specific blood"""
    print(
        "You are only allow to update price of product (you are currently updating blood)"
    )
    continue_ = (
        get_string("Do you want to continue (y/n): ").strip().lower().startswith("y")
    )
    if not continue_:
        return

    product_id = ask_product_id()
    new_blood_price = ask_product_price()

    set_product_price(database, new_blood_price, product_id, "BLOOD")


def update_organe(database: DataBase):
    """Update organe price for a specific organe"""
    print(
        "You are only allow to update price of product (you are currently updating ORGANE)"
    )
    continue_ = (
        get_string("Do you want to continue (y/n): ").strip().lower().startswith("y")
    )
    if not continue_:
        return

    product_id = ask_product_id()
    new_organe_price = ask_product_price()

    set_product_price(database, new_organe_price, product_id, "ORGANE")


def update_type_delivery(database: DataBase):
    """Update/insert type delivery price for a specific type delivery"""
    is_insert = (
        get_string("Do you want to insert a new type of delivery (y/n): ")
        .strip()
        .lower()
        .startswith("y")
    )

    if is_insert:
        new_type_delivery_price = ask_product_price()
        with database as db:
            db.execute("SELECT id FROM TYPE_DELIVERY")
            used_id = db.table
            new_type_delivery_name = "normal"
            while new_type_delivery_name in used_id:
                new_type_delivery_name = get_string("Enter the type of delivery: ")

            db.execute(
                f"INSERT INTO TYPE_DELIVERY (id, price) VALUES ({new_type_delivery_name}, {new_type_delivery_price})",
            )

        print("New type of delivery inserted")
        return

    print(
        "You are only allow to update price of product (you are currently updating TYPE_DELIVERY)"
    )

    # on TYPE_DELIVERY the id is a string
    product_id = "b" * 17
    while not (0 < len(product_id) < 16):
        product_id = get_string("Enter the type of delivery: ")

    new_type_delivery_price = ask_product_price()

    set_product_price(database, new_type_delivery_price, product_id, "TYPE_DELIVERY")

    print("Product type delivery updated")


def insert_menu(database: DataBase):
    """Menu to insert new product in the database

    Args:
        database (DataBase): database to insert product in, connected as accuntant user
    """
    def print_menu():
        print("What do you want to insert ?")
        print("1: BLOOD\n2: ORGANE\n3: DONATOR\n4: EXIT")
    donator_id = None
    blood_id = None
    while True:
        print_menu()
        table = (
            get_string("Enter your choice: ")
            .strip()
            .upper()
        )

        match table:
            case "1":
                blood_id = insert_blood(database)
                continue
            case "2":
                new_donator = (
                    get_string("Is this a new donator (y/n): ")
                    .strip()
                    .lower()
                    .startswith("y")
                )
                if new_donator:
                    donator_id = insert_donator(database)
                insert_organ(database, donator_id)
                continue
            case "3":
                new_blood = (
                    get_string("Is this a new blood (y/n): ")
                    .strip()
                    .lower()
                    .startswith("y")
                )
                if new_blood:
                    blood_id = insert_blood(database)
                donator_id = insert_donator(database, blood_id)
                continue
            case "4":
                return
            case other:
                case_other()


def insert_blood(database: DataBase):
    """Insert blood in the database

    Args:
    -----
        database (DataBase): database to insert blood in, connected as accuntant user

    Return:
    -------
        int: id of the blood inserted
    """
    type: str = ask_product_type()
    signe: str = get_string("Enter the blood signe: (+/-)").strip().lower()
    signe: bool = signe == "+"
    expiration: Date = get_date("Enter the expiration date (YYYY-MM-DD): ", before=Date.today())
    # quantity: float | int = ask_blood_quantity() # TODO: delete 500ml by default
    quantity: float | int = 500

    id = insert_into(
                    database=database, 
                    table="BLOOD", 
                    attributes=("type", "signe", "expiration_date", "quantity"), 
                    values=(type, signe, expiration, quantity)
    )

    logging.info("Blood inserted")
    return id


def insert_organ(database: DataBase, donator_id: int = None):
    """Create new organ in the database

    Ask to user and call insert_into function to insert in the database

    Args:
    -----
        database (DataBase): database to insert organ in, connected as accountant user
        donator_id (int, optional): Id of the donator. Defaults to None.
    """
    if donator_id is None or donator_id < 0:
        print("To insert an organ, you need to insert a donator first")
        donator_id = insert_donator(database)
        print("Back to organ insertion")
    
    state = ask_organ_state()
    funcitonnal = (
        get_string("Get the organ is functional (y/n): ")
        .strip()
        .lower()
        .startswith("y")
    )
    expiration_date_transplantation = get_date(
        "Enter the expiration date for transplantation (YYYY-MM-DD): ", before=Date.today()
    )
    expiration_date = get_date(
        "Enter the expiration date (YYYY-MM-DD): ", before=expiration_date_transplantation
    )
    method_of_conservation = ask_organ_conservation_method()
    type = ask_product_type(True)
    price = ORGAN_DICO[type][0]
    if state == "very well":
        pass
    elif state == "well":
        price *= 0.9
    elif state == "good":
        price *= 0.85
    elif state == "bad":
        price *= 0.8
    elif state == "very bad":
        price *= 0.7
    elif state == "unknown":
        price *= 0.5
    else:
        raise ValueError("state is not correct")

    # does not keep the id of row inserted because accountant does not need it
    insert_into(
        database=database,
        table="ORGANE",
        attributes=("state", "expiration_date", "expiration_date_transplantation", "type", "price", "method_of_preservation", "functional", "Com_id"),
        values=(state, expiration_date, expiration_date_transplantation, type, price, method_of_conservation, funcitonnal, donator_id)
    )
    
    logging.info("Organ inserted")


def insert_donator(database: DataBase, blood_id: int = None):
    """Insert donator in the database

    Args:
        database (DataBase): database to insert donator in, connected as accuntant user

    Returns:
        int: id of the donator inserted
    """

    if blood_id is None or blood_id < 0:
        print("To insert donator, you have to insert a blood first")
        blood_id = insert_blood(database)
        print("Back in insert donator")

    gender = get_string("Gender of the donator (m/f): ").strip().lower().startswith("f")
    age_of_death = ask_age_of_death()

    donator_id =insert_into(
        database=database,
        table="DONATOR",
        attributes=("Giv_id", "gender", "age_range"),
        values=(blood_id, gender, age_of_death),
    )

    logging.info("Donator inserted")

    return donator_id


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
        print("5: Back")

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
            case "5":
                return
            case other:
                case_other()


def select_selling_quantity(database: DataBase):
    """Select the quantity of selling

    Args:
    ----
        database (DataBase): database to select from, connected as accuntant user
    """
    start_date = None
    end_date = None
    
    include_start_date = (
        get_string("Enter a start date (y/n) (if no, start from begin): ")
        .strip()
        .lower()
        .startswith("y")
    )
    if include_start_date:
        start_date = get_date(
            "Enter a start date (YYYY-MM-DD): ", end=Date.today()
        )

    include_end_date = (
        get_string("Enter a end date (y/n) (if no, end at today): ")
        .strip()
        .lower()
        .startswith("y")
    )
    if include_end_date:
        end_date = get_date(
            "Enter a end date (YYYY-MM-DD): ", start=start_date, end=Date.today()
        )

    print("Here is the total of selling for transplantation:")
    querry = "SELECT COUNT(*) as 'Transplantation quantity', SUM(price) as 'Total price for those operation'"
    querry += "FROM TRANSPLANTATION"
    if include_start_date or include_end_date:
        querry += " WHERE "
    if include_start_date:
        querry += f"TRANSPLANTATION.date >= {start_date}"
        if include_end_date:
            querry += " AND "
    if include_end_date:
        querry += f"TRANSPLANTATION.date <= {end_date}"
    querry += ";"

    with database as db:
        db.execute(querry)
        for operations in db.table:
            print(operations)

    print("\n================================\n")
    print("Here is the total of selling for detail (BLOOD):")
    querry = f"SELECT COUNT(*) as 'Detail quantity', SUM({BLOOD_PRICE_FACTOR}) as 'Total price for those details'"
    querry += " FROM DETAIL, BLOOD WHERE"
    if include_start_date or include_end_date:
        querry += " DETAIL.id IN (SELECT ORDER_.id FROM ORDER_ WHERE ORDER_.Buy_id IN (SELECT DELIVERY.id FROM DELIVERY WHERE "
        if include_start_date:
            querry += f"DELIVERY.departure_date >= {start_date}"
            if include_end_date:
                querry += " AND "
        if include_end_date:
            querry += f"DELIVERY.departure_date <= {end_date}"
        querry += ")) AND"
    querry += " DETAIL.BLOOD IS NOT NULL AND DETAIL.BLOOD = BLOOD.id"
    querry += ";"

    with database as db:
        db.execute(querry)
        for operations in db.table:
            print(operations)

    print("\n================================\n")
    print("Here is the total of selling for detail (ORGANE):")
    querry = "SELECT COUNT(*) as 'Detail quantity', SUM(ORGANE.price) as 'Total price for those operation'"
    querry += " FROM DETAIL, ORGANE WHERE"
    if include_start_date or include_end_date:
        querry += " DETAIL.id IN (SELECT ORDER_.id FROM ORDER_ WHERE ORDER_.Buy_id IN (SELECT DELIVERY.id FROM DELIVERY WHERE "
        if include_start_date:
            querry += f"DELIVERY.departure_date >= {start_date}"
            if include_end_date:
                querry += " AND "
        if include_end_date:
            querry += f"DELIVERY.departure_date <= {end_date}"
        querry += ")) AND"
    querry += " DETAIL.ORGANE IS NOT NULL AND DETAIL.ORGANE = ORGANE.id"
    querry += ";"

    with database as db:
        db.execute(querry)
        for operations in db.table:
            print(operations)


def select_product_not_sell(database: DataBase):
    """print products (organs and blood) that are not sell

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


def find_where_are_the_clients(database: DataBase):
    """Find where are the clients and print there address

    Args:
    -----
        database (DataBase): database object connected for this user
    """
    querry = ""
    querry += "SELECT CUSTOMER.id AS 'Customer id', ADDRESS.street AS 'Street', ADDRESS.city AS 'City', ADDRESS.postal_code AS 'Postal code', ADDRESS.land AS 'Country'"
    querry += " FROM CUSTOMER, PERSON, ADDRESS WHERE CUSTOMER.id = PERSON.id AND PERSON.Liv_id = ADDRESS.id"
    querry += " AND PERSON.id IN (SELECT ORDER_.Buy_id FROM ORDER_);"
    with database as db:
        db.execute(querry)

        for row in db.table:
            print(row)


def get_selling_price_of_each_command(database: DataBase):
    """Get the selling price of each command

    Args:
    ----
        database (DataBase): database object connected for this user
    """
    start_date = None
    end_date = None
    
    include_start_date = (
        get_string("Enter a start date (y/n) (if no, start from begin): ")
        .strip()
        .lower()
        .startswith("y")
    )
    if include_start_date:
        start_date = get_date(
            "Enter a start date (format: YYYY-MM-DD): ", end=Date.today()
        )

    include_end_date = (
        get_string("Enter a end date (y/n) (if no, end at today): ")
        .strip()
        .lower()
        .startswith("y")
    )
    if include_end_date:
        end_date = get_date(
            "Enter a end date (format: YYYY-MM-DD): ", before=start_date, end=Date.today()
        )

    print("Here is the client that buy something:")
    querry = f"SELECT ORDER_.id AS 'COMMANDE', SUM(ORGAN.price) AS 'Price organ', SUM({BLOOD_PRICE_FACTOR}) AS 'Price blood', SUM(ORGAN.price) + SUM({BLOOD_PRICE_FACTOR}) AS 'Total price'"
    querry += f"FROM ORDER_, DETAIL, ORGAN, BLOOD WHERE "
    querry += (
        "ORDER_.id = DETAIL.id AND DETAIL.ORGAN = ORGAN.id AND DETAIL.BLOOD = BLOOD.id "
    )
    if include_start_date or include_end_date:
        querry += " AND "
    if include_start_date:
        querry += f"ORDER_.id IN (SELECT DELIVERY.id FROM DELIVERY WHERE DELIVERY.departure_date >= {start_date})"
        if include_end_date:
            querry += " AND "
    if include_end_date:
        querry += f"ORDER_.id IN (SELECT DELIVERY.id FROM DELIVERY WHERE DELIVERY.departure_date <= {end_date})"
    querry += " GROUP BY ORDER_.id;"

    with database as db:
        db.execute(querry)
        for operations in db.table:
            print(operations)
