from exception.usergroupinvalidexception import UserGroupInvalidException
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
    def userGroup(self):
        return self.__type
    
    @property
    def email(self):
        return self.__email

    def addUserGroup(self, userGroup):
        if userGroup in ["CEO", "DOCTOR", "NURSE", "ACCOUNTANT", "ANAESTHESIST", "HR", "CUSTOMER"]:
            self.__type.append(userGroup)
        else:
            raise UserGroupInvalidException(f"UserGroup {userGroup} is not valid")
    
