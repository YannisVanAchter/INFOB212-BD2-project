# encoding uft-8
"""Provide the main menu for the accountant"""
__author__  = ["Yannis Van Achter"]
__version__ = "1.5.0"
__date__    = "2021-05-01"

from datetime import date as Date
import logging
import time

from module.get import get_int, get_string, get_date, get_valid_id
from module.database import DataBase
from module.utils import clear_terminal as cls, insert_into, print_selection
from constants import BLOOD_PRICE_FACTOR, ORGAN_DICO

from .view import *
from .controler import set_product_price


def main_accounting_menu(database: DataBase) -> int:
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
        print("1: BLOOD\n2: TYPE_DELIVERY (allow insert)\n3: EXIT")

    while True:
        print_menu()
        choice = get_string().strip().lower()

        match choice:
            case "1":
                update_blood()
                return
            case "2":
                update_type_delivery(database)
                return
            case "3":
                return
            case _:
                case_other()


def update_blood():
    """Update blood price for a specific blood"""
    print(
        "You are only allow to update price of product (you are currently updating blood)",
        "\nNote that you will update price for every blood at the same time ⚠️",
        "\nAs student project, it is avalable only while running the program, this is not synchronise with a database",
    )
    continue_ = (
        get_string("Do you want to continue (y/n): ").strip().lower().startswith("y")
    )
    if not continue_:
        return

    new_blood_price = ask_product_price()

    BLOODPOCHE = new_blood_price


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

        # check if id is already used and ask for an unused id
        with database as db:
            db.execute("SELECT id FROM TYPE_DELIVERY")
            used_id = db.table
            new_type_delivery_name = "normal"
            while new_type_delivery_name in used_id:
                new_type_delivery_name = get_string("Enter the type of delivery: ")
            
            estimeted_day_of_delivery = -1
            while estimeted_day_of_delivery <= 0:
                estimeted_day_of_delivery = get_int("Enter the estimated day of delivery: ")

        insert_into(
            database=database,
            table="TYPE_DELIVERY",
            attributes=("id", "price", "estimated_days"),
            values=(new_type_delivery_name, new_type_delivery_price, estimeted_day_of_delivery),
        )

        logging.info("New type of delivery inserted")
        return

    print(
        "You are only allow to update price of product (you are currently updating TYPE_DELIVERY)"
    )

    # on TYPE_DELIVERY the id is a string so we can not use get_valid_id()
    product_id = "b" * 17
    with database as db:
        product_id = get_string("Enter the type of delivery: ")
        db.execute_with_params("SELECT id FROM TYPE_DELIVERY WHERE id= %s;", [product_id])
        while len(db.tableArgs) == 0:
            print("This type of delivery does not exist")
            product_id = get_string("Enter the type of delivery: ")
            db.execute_with_params("SELECT id FROM TYPE_DELIVERY WHERE id= %s;", [product_id])

    while True:
        print("1: Update price\n2: Update estimated days")
        choice = get_string("Enter your choice: ").strip().lower()
        
        if choice == "1":
            new_type_delivery_price = ask_product_price()

            set_product_price(database, new_type_delivery_price, product_id, "TYPE_DELIVERY")

            logging.info("Product type delivery updated")
            return 
        elif choice == "2":
            estimeted_day_of_delivery = -1
            while estimeted_day_of_delivery <= 0:
                estimeted_day_of_delivery = get_int("Enter the estimated day of delivery: ")
            
            with database as db:
                db.execute_with_params(
                    "UPDATE TYPE_DELIVERY SET estimated_days=%s WHERE id=%s;",
                    [estimeted_day_of_delivery, product_id]
                )
            logging.info("Product type delivery updated")
            return 
        else:
            case_other()

def insert_menu(database: DataBase):
    """Menu to insert new product in the database

    Args:
        database (DataBase): database to insert product in, connected as accuntant user
    """
    def before_insert(database: DataBase):
        print_selection(database, "SELECT id, gender, age_range FROM DONATOR;", [" id ", "  gender  ", "  age  "])
        return get_valid_id(database, "Current stored id is invalid, please enter an id\nEnter the id of the donator: ", "DONATOR")

    def print_menu():
        print("What do you want to insert ?")
        print("1: BLOOD\n2: ORGANE\n3: DONATOR\n4: EXIT")

    donator_id = None
    blood_id = None
    while True:
        print_menu()
        table = get_string("Enter your choice: ").strip().upper()

        match table:
            case "1":
                new_donator = (
                    get_string("Is this a new donator (y/n): ")
                    .strip()
                    .lower()
                    .startswith("y")
                )
                if new_donator:
                    donator_id = insert_donator(database)
                elif donator_id is None or donator_id < 0:
                    donator_id = before_insert(database)
                blood_id = insert_blood(database, donator_id)
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
                elif donator_id is None or donator_id < 0:
                    donator_id = before_insert(database)
                insert_organ(database, donator_id)
                continue
            case "3":
                donator_id = insert_donator(database, blood_id)
                continue
            case "4":
                return
            case other:
                case_other()


def insert_blood(database: DataBase, donator_id: int = None):
    """Insert blood in the database

    Args:
    -----
        database (DataBase): database to insert blood in, connected as accuntant user

    Return:
    -------
        int: id of the blood inserted
    """
    if donator_id is None or donator_id < 0:
        print("To insert some blood, you need to insert a donator first")
        donator_id = insert_donator(database)
        print("Back to organ insertion")
    
    type: str = ask_product_type()
    signe: str = get_string("Enter the blood signe: (+/-)").strip().lower()
    signe: bool = signe == "+"
    expiration: Date = get_date(
        "Enter the expiration date (YYYY-MM-DD): ", before=Date.today()
    )
    price = BLOOD_PRICE_FACTOR

    id = insert_into(
        database=database,
        table="BLOOD",
        attributes=("type", "signe", "expiration_date", "price", "donator"),
        values=(type, signe, expiration, price, donator_id),
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
        "Enter the expiration date for transplantation (YYYY-MM-DD): ",
        before=Date.today(),
    )
    expiration_date = get_date(
        "Enter the expiration date (YYYY-MM-DD): ",
        before=expiration_date_transplantation,
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
        attributes=(
            "state",
            "expiration_date",
            "expiration_date_transplantation",
            "type",
            "price",
            "method_of_preservation",
            "functionnal",
            "Com_id",
        ),
        values=(
            state,
            expiration_date,
            expiration_date_transplantation,
            type,
            price,
            method_of_conservation,
            funcitonnal,
            donator_id,
        ),
    )

    logging.info("Organ inserted")


def insert_donator(database: DataBase):
    """Insert donator in the database

    Args:
        database (DataBase): database to insert donator in, connected as accuntant user

    Returns:
        int: id of the donator inserted
    """

    gender = get_string("Gender of the donator (m/f): ").strip().lower().startswith("f")
    age_of_death = ask_age_of_death()

    donator_id = insert_into(
        database=database,
        table="DONATOR",
        attributes=( "gender", "age_range"),
        values=(gender, age_of_death),
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
        print("3: where are the clients (with order)")
        print("4: where are the clients (with out order)")
        print("5: get selling price of each command/client")
        print("6: annual report with mentual intermediate report")
        print("7: Back")

    while True:
        print_menu()
        search = get_string("Enter you choice: ").strip()

        match search:
            case "1":
                select_selling_quantity(database)
                get_string("Press enter to continue")
                return
            case "2":
                select_product_not_sell(database)
                get_string("Press enter to continue")
                return
            case "3":
                find_where_are_the_clients(database)
                get_string("Press enter to continue")
                return
            case "4":
                find_where_are_the_clients(database, all=True)
                get_string("Press enter to continue")
            case "5":
                get_selling_price_of_each_command(database)
                get_string("Press enter to continue")
                return
            case "6":
                get_annual_report(database)
                get_string("Press enter to continue")
            case "7":
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
        start_date = get_date("Enter a start date (YYYY-MM-DD): ", after=Date.today())

    include_end_date = (
        get_string("Enter a end date (y/n) (if no, end at today): ")
        .strip()
        .lower()
        .startswith("y")
    )
    if include_end_date:
        end_date = get_date(
            "Enter a end date (YYYY-MM-DD): ", start=start_date, after=Date.today()
        )

    print("Here is the total of selling for transplantation:")
    querry = "SELECT COUNT(*) as 'Transplantation quantity', SUM(price) as 'Total price for those operation'"
    querry += "FROM TRANSPLANTATION"
    if include_start_date or include_end_date:
        querry += " WHERE "
    if include_start_date:
        querry += f"TRANSPLANTATION.date_ >= {start_date}"
        if include_end_date:
            querry += " AND "
    if include_end_date:
        querry += f"TRANSPLANTATION.date_ <= {end_date}"
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
            querry += f"DELIVERY.departure_date >= '{start_date}'"
            if include_end_date:
                querry += " AND "
        if include_end_date:
            querry += f"DELIVERY.departure_date <= '{end_date}'"
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
            querry += f"DELIVERY.departure_date >= '{start_date}'"
            if include_end_date:
                querry += " AND "
        if include_end_date:
            querry += f"DELIVERY.departure_date <= '{end_date}'"
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


def find_where_are_the_clients(database: DataBase, all = False):
    """Find where are the clients and print there address

    Args:
    -----
        database (DataBase): database object connected for this user
        all (bool): if True, print all clients, else print only clients that have order
    """
    def set_len(string, length):
        """Set the length of the string to length

        Args:
        -----
            string (str): string to set the length
            length (int): length of the string

        Returns:
        --------
            str: string with length length
        """
        logging.debug(f"set_len({string}, {length}): current length: {len(string)}")
        if len(string) > length:
            return string[:length + 3] + '...'
        return string + " " * (length - len(string))
    
    querry = ""
    querry += "SELECT CUSTOMER.id AS 'Customer id', ADDRESS.street AS 'Street', ADDRESS.city AS 'City', ADDRESS.postal_code AS 'Postal code', ADDRESS.land AS 'Country'"
    querry += " FROM CUSTOMER, PERSON, ADDRESS WHERE CUSTOMER.id = PERSON.id AND PERSON.Liv_id = ADDRESS.id"
    if not all:
        querry += " AND PERSON.id IN (SELECT ORDER_.Buy_id FROM ORDER_);"
    else:
        querry += ";"
    
    with database as db:
        db.execute(querry)
        
        grouped = dict()
        
        print("| id |      Street      |    City    | Postal code |  Country  |")
        print("+----+------------------+------------+-------------+-----------+")
        # as list of tuple: (id, street, city, postal_code, country)
        # use destructuring  to get variable named id, street, city, postal_code and country
        for (id, street, city, postal_code, country) in db.table:
            id = set_len(str(id), 4)
            street = set_len(str(street), 12)
            city = set_len(str(city), 12)
            postal_code = set_len(str(postal_code), 13)
            country = set_len(str(country), 11)
            print(f"|{id}|{street}|{city}|{postal_code}|{country}|")
            
            if country not in grouped.keys():
                grouped[country] = 1
            else:
                grouped[country] += 1
        
        print(  "+----+------------------+------------+-------------+-----------+")
        print("\n================================================================\n")
        print("Here is the number of clients per country:")
        for country, number in grouped.items():
            print(f"{country}: {number}, pourcentage: {(number / len(grouped) * 100):.2f}%")


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
            "Enter a start date (format: YYYY-MM-DD): ", after=Date.today()
        )

    include_end_date = (
        get_string("Enter a end date (y/n) (if no, end at today): ")
        .strip()
        .lower()
        .startswith("y")
    )
    if include_end_date:
        end_date = get_date(
            "Enter a end date (format: YYYY-MM-DD): ",
            before=start_date,
            after=Date.today(),
        )

    print("Here is the client that buy something:")

    # build querry of clients order
    querry = f"SELECT ORDER_.id AS 'COMMANDE', SUM(ORGANE.price) AS 'Price organ', SUM({BLOOD_PRICE_FACTOR}) AS 'Price blood', SUM(ORGANE.price) + SUM({BLOOD_PRICE_FACTOR}) AS 'Total price'"
    querry += f"FROM ORDER_, DETAIL, ORGANE, BLOOD WHERE "
    querry += "ORDER_.id = DETAIL.id AND DETAIL.ORGANE = ORGANE.id AND DETAIL.BLOOD = BLOOD.id "
    if include_start_date or include_end_date:
        querry += " AND "
    if include_start_date:
        querry += f"ORDER_.id IN (SELECT DELIVERY.id FROM DELIVERY WHERE DELIVERY.departure_date_ >= {start_date})"
        if include_end_date:
            querry += " AND "
    if include_end_date:
        querry += f"ORDER_.id IN (SELECT DELIVERY.id FROM DELIVERY WHERE DELIVERY.departure_date_ <= {end_date})"
    querry += " GROUP BY ORDER_.id;"

    with database as db:
        db.execute(querry)
        for operations in db.table:
            print(operations)
