from module import DataBase
from auth import register, login, become_customer, User
from menu import main_login_menu
from menu import logged_login_menu

def register_action(db: DataBase) -> bool:
    """Register a user and return wether we should log them in automatically or not."""
    email = input("Enter your email address:")
    password = input("Enter the password you wish to create:")
    birthDate = input("Enter your date of birth (format: DD/MM/YYYY):")
    while not _birthDateValidation(birthDate):
        birthDate = input("Birth date intered incorrect, please follow the format DD/MM/YYYY:")
    
    street = input("Enter the street you're living on (without the number):")
    number = input("Enter the number of your home")
    postalCode = input("Enter your postal code:")
    while not _intValidation(postalCode):
        postalCode = input("Postal code invalid, please try again:")
    city = input("Enter your city:")
    land = input("Enter your country:")

    address = {
        "street": street,
        "number": number,
        "postalCode": postalCode,
        "city": city,
        "land": land
    }

    lastName = input("Enter your last name (optional, leave blank if you don't wish to share):")
    if len(lastName) == 0:
        lastName = None
    firstName = input("Enter your first name (optional, leave blank if you don't wish to share):")
    if len(firstName) == 0:
        firstName = None
    phoneNumber = input("Enter your phone number (optional, leave blank if you don't wish to share):")
    if len(phoneNumber) == 0:
        phoneNumber = None

    isRegisteringAsCustomer = input("Do you wish to register for a client account now? (y/n)")

    if isRegisteringAsCustomer == "y":
        nickname = input("Enter your customer nickname:")
        bloodType = input("Enter your blood type (A, B, AB, O):")
        while bloodType not in ["A", "B", "AB", "O"]:
            bloodType = input("Blood type invalid, try again:")
        bloodSign = input("Enter your blood sign (+,-):")
        while not bloodSign in ["+", "-"]:
            bloodSign = input("Blood sign invalid, try again:")
        
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

def _birthDateValidation(birthDate: str) -> bool:
    birthDateSplit = birthDate.split("/")
    if len(birthDateSplit) != 3:
        return False
    if len(birthDateSplit[0]) != 2 or len(birthDateSplit[1]) != 2 or len(birthDateSplit[2]) != 4:
        return False
    for i in range(3):
        try:
            int(birthDateSplit[i])
        except ValueError:
            return False
    return True

def login_action(db: DataBase) -> User | None:
    email = input("What is your email address?")
    password = input("What is your password?")

    user = login(db, email, password)
    if user == None:
        print("Invalid credentials.")
        main_login_menu(db)
    # Call next menu
    return user

def become_customer_action(db: DataBase, user: User):
    # def become_customer(db: DataBase, personId: int, nickname: str, bloodType: str, bloodSign: str):

    nickname = input("Enter your desired nickname")

    bloodTypeValid = False
    while not bloodTypeValid:
        bloodType = input("Entrez le type de votre groupe sanguin (A/B/AB/O)")
        if bloodType in ["A", "B", "AB", "O"]:
            bloodTypeValid = True
        else:
            print("Type invalide, réessayez")

    bloodSignValid = False
    while not bloodSignValid:
        bloodSign = input("Entrer le signe de votre groupe sanguin (+/-)")
        if bloodSign in ["+", "-"]:
            bloodSignValid = True
            bloodSign = bloodSign == "+"
    
    become_customer(db, user.id, nickname, bloodType, bloodSign)
    user.addUserGroup("CUSTOMER")

    
    