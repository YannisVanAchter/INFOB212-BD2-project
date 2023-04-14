from ..module import get_int
from ..auth import User

from module.database import DataBase

def main_login_menu(database: DataBase):
    """Affiche le menu permettant de se connecter

    allow user to:
    --------------
        - S'inscrire
        - Se connecter

    Args:
    -----
        database (DataBase): Data base connected for this user (the accountent)
    """
    print("Bienvenue chez Adopte ton mort. Que souhaitez vous faire ?")
    print("1. Se connecter")
    print("2. S'inscire")

    input_valid = False
    while not input_valid:
        choice = get_int("")

        if choice == 1:
            input_valid = True
            pass
        elif choice == 2:
            input_valid = True
            pass
        else:
            print("Votre sélection n'est pas valide, réessayez.")

def logged_login_menu(database: DataBase, user: User):
    """Affiche le sous menu une fois connecté

    allow user to:
    --------------
        - Modifier son profil
        - Accéder aux autres menus dépendamment de ses permissions

    Args:
    -----
        database (DataBase): Data base connected for this user (the accountent)
    
    """