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

    if email == "Anonymized":
        return None

    query = "SELECT password FROM PERSON WHERE email = %s;"
    db.execute_with_params(query, [email])
    passwordFromDb = db.tableArgs[0][0]
    userGroups = []

    if passwordFromDb == password:
        query = "SELECT id FROM PERSON WHERE email = %s;"
        db.execute_with_params(query, [email])
        userId = db.tableArgs[0][0]
    else:
        return None

    # Check if the user is a customer

    query = "SELECT id FROM CUSTOMER WHERE id = %s;"
    db.execute_with_params(query, [userId])
    if len(db.tableArgs) > 0:
        userGroups.append("CUSTOMER")

    query = "SELECT id FROM STAFF WHERE id = %s;"
    db.execute_with_params(query, [userId])
    if len(db.tableArgs) > 0:
        userGroups.append("STAFF")
        for i in ("CEO", "DOCTOR", "NURSE", "ACCOUNTANT", "ANAESTHESIST", "HR"):
            if _checkIfUserIsSpecificStaff(db, userId, i):
                userGroups.append(i)
    user = User(email, userId, userGroups)
    return user

def _checkIfUserIsSpecificStaff(db: DataBase, userId: int, table: str):
    query = f"SELECT id FROM {table} WHERE id = %s;"
    db.execute_with_params(query, [userId])
    return len(db.tableArgs) > 0

def register(
        db: DataBase,
        email: str, 
        password: str, 
        birthDate: str, 
        address: dict, 
        lastName: str = None, 
        firstName: str = None, 
        phoneNumber: str = None, 
        registerCustomer: dict = None,
        selfLogin=False
    ) -> User | int | None:
    """Register a user in the databse
    
    Args:
    -----
        email: Email of the user to register (str)
        password: Password of the user to register (str)
        birthDate: Date of birth of the user (DD/MM/YYYY) (str)
        address: Dict representing the address (dict)
            street: Street of the address (str)
            number: Number of the address (str)
            postalCode: Postal code of the address (int)
            city: City of the address (str)
            land: Land of the address (str)
        lastName: Last name of the client (str, optional)
        firstName: Frist name of the client (str, optional)
        phoneNumber: Phone number of the client (str, optional)
        registerCustomer: Customer information dict if user wish to create a customer account drectly (dict, optional)
            nickname: Nickname for the customer (str, optional)
            bloodType: Blood type of the customer (str, optional)
            bloodSign: Blood sign of the customer (str, optional) 
        selfLogin: Auto login and returns the User (bool, optional)

    Returns:
    --------
        personId: Id of the person registered
        or
        User: User object of the logged in user
    
    """
    if email == "Anonymized":
        return None
    addressId = db.execute_with_params("INSERT INTO ADDRESS (street, number, postal_code, city, land) VALUES (%s,%s,%s,%s,%s);", 
        (address["street"], address["number"], address["postalCode"], address["city"], address["land"])
    )

    print(addressId)

    args = ["email", "born_date", "password", "Liv_id"]
    print(birthDate)
    birthDateTemp = birthDate.split("/")
    birthDateTemp.reverse()
    print(birthDateTemp)
    birthDateFormatted = "-".join(birthDateTemp)
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
    argsValueForQuery = ("%s," * len(argsValue))[:-1]
    print(f"{argsForQuery=}\n{argsValueForQuery=}\n{argsValue=}")
    query = f"INSERT INTO PERSON ({argsForQuery}) VALUES ({argsValueForQuery});"
    print(query)

    db.execute_with_params(query, tuple(argsValue))

    personId = db.last_row_id

    if registerCustomer != None:
        become_customer(db, personId, registerCustomer["nickname"], registerCustomer["bloodType"], registerCustomer["bloodSign"])

    if selfLogin:
        return login(email, password)
    return personId

def become_customer(db: DataBase, personId: int, nickname: str, bloodType: str, bloodSign: str):
    """Create a new customer based on a person
    
    """
    db.execute_with_params("INSERT INTO CUSTOMER (id, pseudo, blood_type, blood_sign) VALUES (%s,%s,%s,%s)", (personId, nickname, bloodType, bloodSign))

def remove_user(db: DataBase, userId: int) -> str | True:
    """
    Remove a user from the database.

    If it couldn't be deleted, the reason is returned as a string otherwise True is returned.
    """
    queryIsStaff = "SELECT id FROM STAFF WHERE id = %s;"
    db.execute_with_params(queryIsStaff, [userId])
    if len(db.tableArgs) > 0:
        return "Can't delete your account when you're a staff member."
    
    queryUpdate = "UPDATE PERSON SET last_name = 'Anonymized',first_name = 'Anonymized' email = 'Anonymized', phone_number = 'Anonymized', born_date = '1970-01-01', Liv_id = 1 WHERE id = %s;"
    db.execute_with_params(queryUpdate, [userId])

    return True
