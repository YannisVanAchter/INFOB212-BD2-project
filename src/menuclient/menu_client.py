from module import DataBase
from module import get_int, get_string
from auth import User
from constants import ORGAN_DICO, BLOOD_PRICE_FACTOR
import math
from typing import Union
import time
from module import insert_into
from datetime import datetime, timedelta

def main_menu_customer(db: DataBase, user: User = None):
    def print_menu():
        print("What do you want to do?")
        print("1. Buy an organ")
        print("2. Buy blood")
        print("3. See shopping cart")
        print("4. Confirm order")
        print("5. Cancel")


    cart = []
    order_confirmed = False

    while not order_confirmed:
        print_menu()
        choice = get_int("\n")

        if choice == 1:
            organ = add_organ_to_cart(db)
            if organ != None:
                cart.append({"type": "organ", "undertype": organ["type"], "id": organ["id"], "price": organ["price"]})
        elif choice == 2:
            blood = add_blood_to_cart(db)
            if blood != None:
                for id in blood[0]:
                    cart.append({"type": "blood", "undertype": blood[1], "id": id, "price": 250})
        elif choice == 3:
            _print_shopping_cart(cart)
        elif choice == 4:
            order_confirmed = True
            confirm_order(db, cart, user)
            print(cart)
        elif choice == 5:
            return
        else:
            print("Invalid choice")


def confirm_order(db: DataBase, cart: list, user: User):
    delivery_id = create_delivery(db, user)
    # Create order
    order_id = insert_into(
        database=db,
        table="ORDER_",
        attributes=("Typ_id", "Buy_id"),
        values=(delivery_id, user.id)
    )
    for item in cart:
        if item["type"] == "organ":
            pass
        elif item["type"] == "blood":
            pass

def create_delivery(db: DataBase, user: User) -> int:
    today_date = datetime.now()

    # Get delivery and expected date
    db.execute("SELECT id, price, estimated_days FROM TYPE_DELIVERY ORDER BY PRICE DESC")
    all_delivery_type = db.table

    display_available_delivery_type(all_delivery_type)

    delivery_choice_valid = False
    while not delivery_choice_valid:
        delivery_choice = get_int("Enter the number corresponding to the delivery method of your choosing.")
        if delivery_choice == 0 or delivery_choice > len(all_delivery_type):
            print("Delivery type invalid, please try again")
        else:
            delivery_choice_valid = True

    delivery_type_id = all_delivery_type[delivery_choice - 1][0]
    expected_delivery = today_date + timedelta(days=all_delivery_type[delivery_choice - 1][2])

    # Get name
    first_name = get_string("What is the first name we should put on for the delivery?")
    last_name = get_string("What is the last name we should put on for the delivery?")

    # Get address

    db.execute_with_params("SELECT Liv_id FROM PERSON WHERE id = %s", [user.id])
    address_id = db.tableArgs[0][0]

    return insert_into(
        database=db, 
        table="DELIVERY",
        attributes=("departure_date", "arrival_date", "recipent_last_name", "recipent_first_name", "Typ_id", "At_id"),
        values=(today_date.strftime("%Y-%m-%d"), expected_delivery.strftime("%Y-%m-%d"), last_name, first_name, delivery_type_id, address_id)
    )



    
def display_available_delivery_type(types: list[list]):
    print("N°|     Name     | Price | Delivery Time")
    print("----------------------------------------")
    index = 1
    for _type in types:
        name = _type[0]
        if len(name) > 14:
            name_display = name[:11] + "...|"
        else:
            name_offset = get_offset(14, name)
            name_display = make_string_with_offset(name, name_offset, 14) + "|"
        
        price = str(_type[1])
        price_offset = get_offset(7, price)
        # print(price_offset)
        price_display = make_string_with_offset(price, price_offset, 7) + "|"

        delivery_time: int = _type[2]
        delivery_time: str = str(delivery_time) + " days"
        delivery_time_offset = get_offset(14, delivery_time)
        delivery_display = make_string_with_offset(delivery_time, delivery_time_offset, 14)
        print(f"{index}.|", name_display, price_display, delivery_display, sep="")
        index += 1



def _print_shopping_cart(cart: list):
    print("Here are all the items currently in your cart:")
    for item in cart:
        print(f"Type: {item['type']} | Undertype: {item['undertype']} | Price: {item['price']}")
    time.sleep(5)


def add_blood_to_cart(db: DataBase) -> (Union[list[int], str] | None):
    blood_type_valid = False
    while not blood_type_valid:
        blood_type = get_string("Enter your blood type: (A/B/AB/O)")
        if blood_type not in ["A", "B", "AB", "O"]:
            print("Invalid, try again.")
        else:
            blood_type_valid = True
    
    blood_sign_valid = False
    while not blood_sign_valid:
        blood_sign = get_string("Enter your blood sign: (+/-)")
        if blood_sign not in ["+", "-"]:
            print("Invalid, try again")
        else:
            blood_sign_valid = True
            blood_sign = blood_sign == "+"

    db.execute_with_params("SELECT COUNT(*) FROM BLOOD B WHERE \
                            B.type = %s AND \
                            B.signe = %s AND \
                            B.expiration_date > CURRENT_DATE() AND \
                            B.Nee_id is null AND B.id not in (\
                                SELECT D.BLOOD FROM DETAIL D WHERE B.id = D.BLOOD\
                            )", [blood_type, blood_sign])
    
    blood_bag_available = db.tableArgs[0][0]
    sign_display = "+" if blood_sign else "-"
    if blood_bag_available == 0:
        print(f"No {blood_type}{sign_display} blood available")
        return None

    bags_wanted = get_int(f"{blood_bag_available} bags available, how many do you want to buy? {BLOOD_PRICE_FACTOR}€/bag")

    if bags_wanted > blood_bag_available:
        confirmation_valid = False
        while not confirmation_valid:
            confirmation = get_string("You asked more than what we have do you want all our stock or do you want to cancel your order? (proceed/cancel)").strip().lower()
            if confirmation not in ["proceed", "cancel"]:
                print("Invalid. Please try again.")
            else:
                confirmation_valid = True
        
        if confirmation == "proceed":
            bags_wanted = blood_bag_available
        else:
            print("Canceling...")
            return None

    # get ids of bought bags
    db.execute_with_params(f"SELECT id FROM BLOOD B WHERE \
                            B.type = %s AND \
                            B.signe = %s AND \
                            B.expiration_date > CURRENT_DATE() AND \
                            B.Nee_id is null AND B.id not in (\
                                SELECT D.BLOOD FROM DETAIL D WHERE B.id = D.BLOOD\
                            ) LIMIT {bags_wanted}", [blood_type, blood_sign])

    all_ids = []

    for row in db.tableArgs:
        all_ids.append(row[0])
    return [all_ids, f"{blood_type}{sign_display}"]

    

def add_organ_to_cart(db: DataBase) -> (dict | None):
    """Ask the user for the organ it wants and returns the id of the organ, its type and its price or None if no organ was chosen
    
    Returns
    -------
    organ dict: id - Id of the organ (int)
                type - Type of the organ (str)
                price - Price of the organ (float)
    """
    print("Available organs: " + ", ".join(ORGAN_DICO.keys()))
    organ_type_choice = get_string("What type of organ do you want?").strip().lower()

    while organ_type_choice not in ORGAN_DICO.keys():
        organ_type_choice = get_string("Invalid organ type, try again.").strip().lower()
    
    # Display available organs of this type

    current_page = 1

    db.execute_with_params("SELECT COUNT(*) FROM ORGANE WHERE type = %s AND ORGANE.id not in\
        (\
	    SELECT Con_id FROM TRANSPLANTATION T WHERE T.Con_id = ORGANE.id\
        ) and ORGANE.id not in (SELECT D.ORGANE FROM DETAIL D WHERE D.ORGANE = ORGANE.id)", [organ_type_choice])
    organ_count = int(db.tableArgs[0][0])
    if organ_count == 0:
        print("No organs available.")
        return None
    
    max_page = math.ceil(organ_count / 5)

    organ_chosen = None

    while organ_chosen == None:
        if current_page > max_page:
            print("No more organ available, strating back from the beginning.")
            current_page = 1

        query = f"SELECT id, state, functionnal, expiration_date, method_of_preservation, price FROM ORGANE WHERE type = %s AND ORGANE.id not in\
        (\
	    SELECT Con_id FROM TRANSPLANTATION T WHERE T.Con_id = ORGANE.id\
        ) and ORGANE.id not in (SELECT D.ORGANE FROM DETAIL D WHERE D.ORGANE = ORGANE.id)\
        ORDER BY price DESC LIMIT 5 OFFSET {(current_page - 1) * 5}"
        db.execute_with_params(query, [organ_type_choice])
        organ_displayed = db.tableArgs
        _display_organ_page(organ_displayed)

        this_choice_valid = False
        while not this_choice_valid:
            this_choice = get_int("Envoyez le chiffre correspondant a l'organe que vous souhaitez. Envoyez 6 si vous souhaitez voir la suite.\n Envoyez 0 si vous souhaitez sortir sans rien acheter")
            if this_choice > len(organ_displayed) and this_choice != 6:
                print("Choix invalide, réessayez.")
            else:
                this_choice_valid = True
        
        if this_choice == 6:
            current_page += 1
        elif this_choice == 0:
            return None
        else:
            return {"id": organ_displayed[this_choice - 1][0], "type": organ_type_choice, "price": organ_displayed[this_choice - 1][5]}

def _display_organ_page(rows: list[list]):
    header = "N°|   State   | Functionnal | Expiration Date |   Method of Preservation   |    Price    |"
    print(header)
    print("-" * len(header))
    index = 1
    for row in rows:
        state_display_offset = get_offset(11, row[1])
        state_display = make_string_with_offset(row[1], state_display_offset, 11) + "|"

        functionnal_display_word = "Yes" if row[2] == 1 else "No"
        functional_display = make_string_with_offset(functionnal_display_word, 5, 5) + "|"

        date_formated = row[3].strftime("%d-%m-%Y")
        expiration_display = f"{' ' * 3}{date_formated}{' ' * 3} |"

        preservation_method = row[4]
        # taille max 28
        if len(row[4]) > 25:
            preservation_method_display = preservation_method[:25] + "...|"
        else:
            preservation_method_offset = get_offset(28, preservation_method)
            preservation_method_display = make_string_with_offset(preservation_method, preservation_method_offset, 28) + "|"
        
        price_str = str(row[5])
        # print(price_str)
        # print(len(price_str))
        price_offset = get_offset(13, price_str)
        price_display = make_string_with_offset(price_str, price_offset, 13) + "|"

        print(f"{index}.|{state_display}{functional_display}{expiration_display}{preservation_method_display}{price_display}")
        index += 1


def get_offset(max_size: int, string: str):
    return math.floor((max_size - len(string)) / 2)

def make_string_with_offset(string: str, offset: int, max_size: int):
    to_return = f"{' ' * offset}{string}{' ' * offset}"
    # print(to_return)
    return f"{to_return}{' ' * (max_size - len(to_return))}"