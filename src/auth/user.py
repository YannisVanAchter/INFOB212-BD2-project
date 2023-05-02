class User:
    """Class représentant un utilisateur.
    
    """

    def __init__(self, email: str, id: int, type: list[str]):
        self.__id = id
        self.__email = email
        self.__type = type # Représente la fonction de l'utilisateur pour les permissions (employés, médecin etc)

    @property
    def id(self):
        return self.__id

    @property
    def logged(self):
        return self.__authenticated
    
    @property
    def userGroup(self):
        return self.__type
    
    @property
    def email(self):
        return self.__email



    
