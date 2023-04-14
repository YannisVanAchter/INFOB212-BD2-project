class User:
    """Class représentant un utilisateur.
    
    """

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.__authenticated = False
        self.__type = None # Représente la fonction de l'utilisateur pour les permissions (employés, médecin etc)
        self.login()

    def login(self):
        """Try to login with the password and email provided."""

    @property
    def logged(self):
        return self.__authenticated
    
    @property
    def userGroup(self):
        return self.__type
    
