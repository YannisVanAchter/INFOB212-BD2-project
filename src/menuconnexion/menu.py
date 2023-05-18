from module import get_int
from auth import User

from module.database import DataBase
from .actions import become_customer_action, login_action, register_action
from menupersonnel.menuaccounting import main_accounting_menu
from menupersonnel.menumédecin import main_anesthesiste_menu, main_infirmier_menu, main_medecin_menu
from menupersonnel.RH import main_RH_menu
from menupersonnel.menuPDG import main_PDG_menu

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
        # utiliser un get_string(...).strip().lower() pour éviter les erreurs de frappe -> lower inutile (chiffre) et strip déjà fait par le cast int
        choice = get_int("")
        if choice == 1:
            input_valid = True
            user = _try_login(database)
        elif choice == 2:
            input_valid = True
            register_action(database)
            print("Inscription enregistrée. Veuillez vous connecter.")
            user = _try_login(database)
        else:
            print("Votre sélection n'est pas valide, réessayez.")
    if user != None:
        logged_login_menu(database, user)

def _try_login(database: DataBase) -> User:
    user = login_action(database)
    attempt = 1
    while user == None:
        print("Identifiant incorrect, réessayez.")
        user = login_action(database)
        attempt += 1
        if attempt > 5:
            print("Trop de tentative, fermeture.")
            exit()
    return user

def logged_login_menu(db: DataBase, user: User):
    """Affiche le sous menu une fois connecté

    allow user to:
    --------------
        - Modifier son profil
        - Accéder aux autres menus dépendamment de ses permissions

    Args:
    -----
        database (DataBase): Data base connected for this user (the accountent)
    
    """
    is_customer = "CUSTOMER" in user.userGroup
    if is_customer:
        print("1. Aller dans le menu client")
    else:
        print("1. Créer un compte client")

    is_accountant = "ACCOUNTANT" in user.userGroup
    if is_accountant:
        print("2. Rejoindre le menu comptable")
    
    is_nurse = "NURSE" in user.userGroup
    if is_nurse:
        print("3. Rejoindre le menu des infirmières")
    
    is_doctor = "DOCTOR" in user.userGroup
    if is_doctor:
        print("4. Rejoindre le menu des médecins")
    
    is_anaesthesist = "ANAESTHESIST" in user.userGroup
    if is_anaesthesist:
        print("5. Rejoindre le menu des anesthésistes")
    
    is_hr = "HR" in user.userGroup
    if is_hr:
        print("6. Rejoindre le menu RH")

    is_ceo = "CEO" in user.userGroup
    if is_ceo:
        print("7. Rejoindre le menu PDG")


    while True:
        user_choice = get_int("Entrer le chiffre correspondant au menu que vous souhaitez")
        error_message = "Vous n'avez pas les permissions pour aller dans ce menu. Réessayez."
        if user_choice == 1:
            if is_customer:
                pass # Envoyer vers le menu client
            else:
                become_customer_action(db, user)
        elif user_choice == 2:
            if is_accountant:
                main_accounting_menu(db)
            else:
                print(error_message)
        elif user_choice == 3:
            if is_nurse:
                main_infirmier_menu(db)
            else:
                print(error_message)
        elif user_choice == 4:
            if is_doctor:
                main_medecin_menu(db)
            else:
                print(error_message)
        elif user_choice == 5:
            if is_anaesthesist:
                main_anesthesiste_menu(db)
            else:
                print(error_message)
        elif user_choice == 6:
            if is_hr:
                main_RH_menu(db)
            else:
                print(error_message)
        elif user_choice == 7:
            if is_ceo:
                main_PDG_menu(db)
            else:
                print(error_message)
