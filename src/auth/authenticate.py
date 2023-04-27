from auth import User
from module import DataBase

def login(db: DataBase, email: str, password: str) -> User | None:
    """Login a user

    Args:
    -----
        email: Email of the user (str)
        password: Password of the user (str)

    Returns:
    --------
    user: User object or None if login details are incorrect.
    
    """

    query = "SELECT password FROM person WHERE email = '%s';"

    db.execute_with_params(query, (email,))
    print(db.tableArgs)

    pass

def register(
        db: DataBase,
        email: str, 
        password: str, 
        birthDate: str, 
        address: dict, 
        lastName: str = None, 
        firstName: str = None, 
        phoneNumber: str = None, 
        selfLogin=False
    ) -> User | int:
    """Register a user in the databse
    
    Args:
    -----
        email: Email of the user to register (str)
        password: Password of the user to register (str)
        birthDate: Date of birth of the user (DD/MM/YYYY) (str)
        address: Dict representing the address (dict)
            street: Street of the address (str)
            number: Number of the address (int)
            postalCode: Postal code of the address (int)
            city: City of the address (str)
            land: Land of the address (str)
        lastName: Last name of the client (str, optional)
        firstName: Frist name of the client (str, optional)
        phoneNumber: Phone number of the client (str, optional)
        selfLogin: Auto login and returns the User (bool, optional)

    Returns:
    --------
        personId: Id of the person registered
        or
        User: User object of the logged in user
    
    """

    db.execute_with_params("INSERT INTO ADDRESS (street, number, postal_code, city, land) VALUES (%s,%s,%s,%s,%s);", 
        (address["street"], address["number"], address["postalCode"], address["city"], address["land"])
    )

    addressId = db.last_row_id

    args = ["email", "born_date", "password", "Liv_id"]
    birthDateFormatted = birthDate.split("/").reverse().join("-")
    argsValue = [email, birthDateFormatted, password, addressId]

    if lastName != None:
        args.append("last_name")
        argsValue.append(lastName)
    if firstName != None:
        args.append("first_name")
        argsValue.append(firstName)
    if phoneNumber != None:
        args.append("phone_number")
        argsValue.append(phoneNumber)

    argsForQuery = ", ".join(args)
    argsValueForQuery = ("%s," * len(argsValue))[::-1]
    print(f"{argsForQuery=}\n{argsValueForQuery=}")
    query = f"INSERT INTO PERSON ({argsForQuery}) VALUES ({argsValueForQuery});"

    db.execute_with_params(query, tuple(argsValue))

    personId = db.last_row_id

    if selfLogin:
        return login(email, password)
    return personId

def register_cutomer(db: DataBase, personId: int, nickname: str, bloodType: str, bloodSign: str):
    """Create a new customer based on a person
    
    """
    db.execute_with_params("INSERT INTO CUSTOMER (id, pseudo, blood_type, blood_sign) VALUES (%s,%s,%s,%s)", (personId, nickname, bloodType, bloodSign))
