class User:
    """Class représentant un utilisateur.
    
    """

    def __init__(self, email: str, password: str):
        self.__id = None
        self.__email = email
        self.__password = password
        self.__type = None # Représente la fonction de l'utilisateur pour les permissions (employés, médecin etc)

    @property
    def logged(self):
        return self.__authenticated
    
    @property
    def userGroup(self):
        return self.__type
    
    @property
    def email(self):
        return self.__email


    
