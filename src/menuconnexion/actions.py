from module import DataBase
from auth import register, login, become_customer

def register_action(db: DataBase):
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
    
    
    register(db, email, password, birthDate, address, lastName, firstName, phoneNumber, )

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

def login_action(db: DataBase):
    pass