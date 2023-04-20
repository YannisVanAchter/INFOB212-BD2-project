from user import User

def login(email: str, password: str) -> User:
    """Login a user

    Args:
    -----
        email: Email of the user (str)
        password: Password of the user (str)

    Returns:
    --------
    user: User object
    
    """
    pass

def register(
        email: str, 
        nickname: str, 
        password: str, 
        birthDate: str, 
        address: dict, 
        bloodType: str, 
        bloodSign: str, 
        lastName: str = None, 
        firstName: str = None, 
        phoneNumber: str = None, 
        selfLogin=False
    ) -> User | None:
    """Register a user in the databse
    
    Args:
    -----
        email: Email of the user to register (str)
        nicname: Nickname of the user (str)
        password: Password of the user to register (str)
        birthDate: Date of birth of the user (DD/MM/YYYY) (str)
        address:
            street: Street of the address (str)
            number: Number of the address (int)
            postalCode: Postal code of the address (int)
            city: City of the address (str)
            land: Land of the address (str)
        bloodType: Type of blood of the client {A, B, AB, O}
        bloodSign: Sign of the blood type of the client {+, -}
        lastName: Last name of the client (str, optional)
        firstName: Frist name of the client (str, optional)
        phoneNumber: Phone number of the client (str, optional)
        selfLogin: Auto login and returns the User (bool, optional)
    
    """


    if selfLogin:
        return login()
    pass