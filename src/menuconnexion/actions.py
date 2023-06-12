from datetime import datetime

from module import DataBase, get_string, get_int
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
    first_name = get_string("First name (If you don't wish to modify it leave blank):")
    last_name = get_string("Last name (If you don't wish to modify it leave blank):")
    email = get_string("Email (If you don't wish to modify it leave blank):")
    phone_number = get_string("Phone number (If you don't wish to modify it leave blank):")
    password = get_string("Password (If you don't wish to modify it leave blank):")
    # Handle the address
    if get_string("Do you wish to change your address? (y/n)").strip().lower().startswith("y"):
        street = get_string("Street (If you don't wish to modify it leave blank):")
        number = get_int("Number (If you don't wish to modify it leave blank):")
        postal_code = get_string("Postal Code (If you don't wish to modify it leave blank):")
        city = get_string("City (If you don't wish to modify it leave blank):")
        land = get_string("Land (If you don't wish to modify it leave blank):")

    if "CUSTOMER" in user.userGroup:
        blood_type = get_string("Blood Type (If you don't wish to modify it leave blank) (A/B/AB/O):")
        blood_sign = get_string("Blood Sign (If you don't wish to modify it leave blank) (+/-):")
        pseudo = get_string("Pseudo (If you don't wish to modify it leave blank):")
    pass

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

    
    