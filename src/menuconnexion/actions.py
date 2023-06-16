from datetime import datetime

from module import DataBase, get_string, get_int, insert_into, print_selection
from auth import register, login, become_customer, User

def register_action(db: DataBase) -> bool:
    """Register a user and return wether we should log them in automatically or not."""
    email = get_string("Enter your email address: ")
    password = get_string("Enter the password you wish to create: ")
    birthDate = get_string("Enter your date of birth (format: DD/MM/YYYY): ")
    while not _birthDateValidation(birthDate, True):
        birthDate = get_string("Birth date incorrect, please follow the format DD/MM/YYYY: ")
    
    street = get_string("Enter the street you're living on (without the number): ")
    number = get_int("Enter the number of your home: ")
    postalCode = get_string("Enter your postal code: ")
    while not _intValidation(postalCode):
        postalCode = get_string("Postal code invalid, please try again: ")
    city = get_string("Enter your city: ")
    land = get_string("Enter your country: ")

    address = {
        "street": street,
        "number": number,
        "postalCode": postalCode,
        "city": city,
        "land": land
    }

    lastName = get_string("Enter your last name: ")
    firstName = get_string("Enter your first name: ")
    phoneNumber = get_string("Enter your phone number (optional, leave blank if you don't wish to share): ")
    if len(phoneNumber) == 0:
        phoneNumber = None

    isRegisteringAsCustomer = get_string("Do you wish to register for a client account now? (y/n): ").lower().strip()

    if isRegisteringAsCustomer.startswith("y"):
        nickname = get_string("Enter your customer nickname:").strip()
        bloodType = get_string("Enter your blood type (A, B, AB, O):").strip().upper()
        while bloodType not in ["A", "B", "AB", "O"]:
            bloodType = get_string("Blood type invalid, try again:").strip().upper()
        bloodSign = get_string("Enter your blood sign (+,-):").strip()
        while not bloodSign in ["+", "-"]:
            bloodSign = get_string("Blood sign invalid, try again:").strip()
        
        registerCustomer = {
            "nickname": nickname,
            "bloodType": bloodType,
            "bloodSign": bloodSign
        }

    

    register(db, email, password, birthDate, address, lastName, firstName, phoneNumber, registerCustomer)

def _intValidation(integer: str) -> bool:
    try:
        int(integer)
    except ValueError:
        return False
    return True

def _birthDateValidation(birthDate: str, check_minor: bool = False) -> bool:
    def is_minor(date_of_birth):
        # get current date
        current_date = datetime.now().date()

        # convert string to date
        date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y').date()

        age = current_date.year - date_of_birth.year

        # Check is minor or not
        if age < 18:
            return True
        else:
            return False
    
    try:
        datetime.strptime(birthDate, '%d/%m/%Y') # check validity of fomat string
        if (check_minor) and (is_minor(birthDate)):
            return False
        
        return True
    except ValueError:
        return False

def login_action(db: DataBase) -> (User | None):
    email = get_string("What is your email ?")
    password = get_string("What is your password?")

    user = login(db, email, password)
    # Call next menu
    return user

def modify_profile_action(db: DataBase, user: User):
    print("Your information: ")
    print_selection(db, 
                    f"SELECT P.first_name, P.last_name, P.email, P.phone_number, P.password FROM PERSON P WHERE P.id = {user.id}", 
                    ["  First name  ", "  Last name  ", "            Email            ", "   Phone number   ", "  Password  "]
        )
    first_name = _returnNoneIfBlank(get_string("First name (If you don't wish to modify it leave blank):"))
    last_name = _returnNoneIfBlank(get_string("Last name (If you don't wish to modify it leave blank):"))
    email = _returnNoneIfBlank(get_string("Email (If you don't wish to modify it leave blank):"))
    phone_number = _returnNoneIfBlank(get_string("Phone number (If you don't wish to modify it leave blank):"))
    password = _returnNoneIfBlank(get_string("Password (If you don't wish to modify it leave blank):"))
    # Handle the address
    modify_address = get_string("Do you wish to change your address? (y/n)").strip().lower().startswith("y")
    if modify_address:
        print_selection(db, 
                        f"SELECT A.street, A.number, A.postal_code, A.city, A.land FROM ADDRESS A, PERSON P WHERE A.id = P.Liv_id AND P.id = {user.id}",
                        ["        Street        ", "Number", "Postal code", "     City     ", "   Land   "]
            )
        street = _returnNoneIfBlank(get_string("Street (If you don't wish to modify it leave blank):"))
        number = _returnNoneIfBlank(get_string("Number (If you don't wish to modify it leave blank):"))
        if number is not None:
            number = int(number)
        postal_code = _returnNoneIfBlank(get_string("Postal Code (If you don't wish to modify it leave blank):"))
        if postal_code is not None:
            postal_code = int(postal_code)
        city = _returnNoneIfBlank(get_string("City (If you don't wish to modify it leave blank):"))
        land = _returnNoneIfBlank(get_string("Land (If you don't wish to modify it leave blank):"))

    is_customer = "CUSTOMER" in user.userGroup
    if is_customer:
        print_selection(db,
                        f"SELECT C.pseudo, C.blood_type, C.blood_sign FROM CUSTOMER C WHERE C.id = {user.id}",
                        ["    Pseudo    ", "Blood type", "Blood sign"]
            )
        
        blood_type = _returnNoneIfBlank(get_string("Blood Type (If you don't wish to modify it leave blank) (A/B/AB/O):"))
        if blood_type is not None:
            if blood_type not in ["A", "B", "AB", "O"]:
                print("Blood type invalid, blood type won't be modified")
                blood_type = None
        blood_sign = _returnNoneIfBlank(get_string("Blood Sign (If you don't wish to modify it leave blank) (+/-):").strip())
        if blood_sign is not None:
            if blood_sign == "+":
                blood_sign = True
            else:
                blood_sign = False
        pseudo = _returnNoneIfBlank(get_string("Pseudo (If you don't wish to modify it leave blank):"))

    person = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "password": password
    }
    
    address = None
    customer = None

    if modify_address:
        address = {
            "street": street,
            "number": number,
            "postal_code": postal_code,
            "city": city,
            "land": land
        }

    if is_customer:
        customer = {
            "blood_type": blood_type,
            "blood_sign": blood_sign,
            "pseudo": pseudo
        }

    update_profile_in_db(db, user, person, address, customer)

def update_profile_in_db(db: DataBase, user: User, person: dict = None, address: dict = None, customer: dict = None):
    """
    Parameters
    ----------
    db: The database object (DataBase)
    user: The user object of the user being modified to modify(User)
    person: A dict containing the person's information to modify (optional)
    address: A dict containing the address's information to modify (optional)
    customer: A dict containing the customer's information to modify (optional)
    """
    
    if person != None:
        edited_person_values = []
        column_query_strs = []
        for column, value in person.items():
            if value is not None:
                column_query_strs.append(f"{column} = %s")
                edited_person_values.append(value)
                    
        if len(column_query_strs) != 0:
            update_query_person = f"UPDATE PERSON SET {', '.join(column_query_strs)} WHERE id = {user.id}"
            db.execute_with_params(update_query_person, edited_person_values)

    # To put in a function to remove redundant code
    if customer != None:
        edited_customer_values = []
        column_query_strs = []
        for column, value in customer.items():
            if value is not None:
                column_query_strs.append(f"{column} = %s")
                edited_customer_values.append(value)

        if len(column_query_strs) != 0:
            update_query_customer = f"UPDATE CUSTOMER SET {', '.join(column_query_strs)} WHERE id = {user.id}"
            db.execute_with_params(update_query_customer, edited_customer_values)

    if address != None:
        # Get the id of the address of this person
        address_id_query = f"SELECT id, street, number, postal_code, city, land FROM ADDRESS WHERE id IN (SELECT Liv_id FROM PERSON WHERE id = {user.id});"
        db.execute(address_id_query)
        address_id = db.table[0][0]
        address_already_used = False # more than one person (another one than current user)
        current_address = {
            "street": db.table[0][1],
            "number": db.table[0][2],
            "postal_code": db.table[0][3],
            "city": db.table[0][4],
            "land": db.table[0][5],
        }
        
        # check address is not already used by another person or a delivery
        nb_use_of_address_query = f"SELECT * FROM ADDRESS WHERE id = {address_id} AND ({address_id} IN (SELECT Liv_id FROM PERSON WHERE id != {user.id}) OR {address_id} IN (SELECT At_id FROM DELIVERY));"
        db.execute(nb_use_of_address_query)
        if len(db.table) != 0:
            address_already_used = True
            
        if address_already_used:
            for column, value in address.items():
                if value is None:
                    address[column] = current_address[column]
                    
            new_address_id = insert_into(db, "ADDRESS", address.keys(), address.values())
            
            db.execute(f"UPDATE PERSON SET Liv_id = {new_address_id} WHERE id = {user.id};")
            
        else:
            edited_address_values = []
            column_query_strs = []
            for column, value in address.items():
                if value is not None:
                    column_query_strs.append(f"{column} = %s")
                    edited_address_values.append(value)
            
                
            if len(column_query_strs) != 0:
                update_query_address = f"UPDATE ADDRESS SET {', '.join(column_query_strs)} WHERE id = {address_id}"
                db.execute_with_params(update_query_address, edited_address_values)


def _returnNoneIfBlank(inp: str):
    if inp == "":
        return None
    else:
        return inp

def become_customer_action(db: DataBase, user: User):
    """Become customer in database

    Args:
    -----
        db (DataBase): DB ready to be connected
        user (User): Current user
        
    Modifie:
    --------
        User.addUserGroup("CUSTOMER")
    """
    nickname = get_string("Enter your pseudo").strip()

    bloodTypeValid = False
    while not bloodTypeValid:
        bloodType = get_string(" Enter your blood type (A/B/AB/O)").upper().strip()
        if bloodType in ["A", "B", "AB", "O"]:
            bloodTypeValid = True
        else:
            print("Invalid, please try again")

    bloodSignValid = False
    while not bloodSignValid:
        bloodSign = input("Enter the sign of your blood group (+/-)").strip()
        if bloodSign in ["+", "-"]:
            bloodSignValid = True
            bloodSign = bloodSign == "+"
        else:
            print("Invelid, please try again")
    
    become_customer(db, user.id, nickname, bloodType, bloodSign)
    user.addUserGroup("CUSTOMER")

    
    