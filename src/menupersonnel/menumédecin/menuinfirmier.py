import datetime
import mysql.connector as mysql
import module.get as get

from module.database import DataBase

"""
La fonction de connection qui appelle celle des menus s'occupe déjà de connecter l'utilisateur
Tu peux demander d'avoir son identifiant et son mot de passe dans ta spécification

Tu peux utiliser le module 'get' pour demander à l'utilisateur de rentrer des informations (pour l'id notament) afin d'améliorer la liste du code.

N'hésite pas non plus a faire de plus petites fonctions pour éviter de trop longues ligne à lire
Cela vas aussi augmenter la lisiblé de ton code
"""

def main_infirmier_menu(database: DataBase):

    """
    Allows a medecin to navigate throughout his patients, his operations and his colleguas according to what he asks
    This function prints what the medecin has aksed for after making requests to the Database
    
    Author: Eline Mota
    """

    print("In médecin menu")
    id = str(input("Quel est votre identifiant d'infirmier ?")) #récupère l'identifiant de l'infirmier

    while True:
        print("Que voulez-vous faire ?")
        print("Tapez 1 si vous voulez voir les personnes avec lesquelles vous travaillez")
        print("Tapez 2 si vous voulez voir les dates de vos futures opérations")
        print("Tapez 3 si vous voulez des informations sur un organe que vous allez transplanter")
        print("Tapez 4 si vous vouez avoir des informations sur un client en particulier")
        print("Tapez 5 ou autre chose si vous désirez arrêter de demander des informations à la base de données")

        numero = int(input("choix:"))

        if numero == 1:
            seepeople(id)
        
        elif numero == 2:
            seedate_operations(id)

        elif numero == 3:
            info_organe()

        elif numero == 4:
            info_client()
        else:
            break

def seepeople(database: DataBase, id):
    """
    Allows a nurse to see people with who he works with according to a date of an operation
    This function prints the id of the anesthesiste and medecin he works with on a certain date
    
    Author: Eline Mota
    """
    database.connect()

    print("Quelle est la date de l'opération dont vous voulez voir les personnes avec qui vous allez travailler ? ")
    annee = int(input("Donnez moi l'année de l'opération"))
    jour = int(input("Donnez moi le jour de l'opération"))
    mois = get.get_int("Donnez moi le mois de l'opération")

    #transforme en date
    date_operation = datetime.date(annee, jour, mois)

    #cherche les anésthésistes qui travaillent avec le médecin à la date donnée et selon l'id du médecin
    anesthésiste = ("SELECT id FROM ANAESTHETIST WHERE id in (SELECT A_w_id from TRANSPLANTATION WHERE date_ = %s AND D_w_id = %s)")

    database.execute(anesthésiste, (date_operation, id))

    print("Voici les personnes avec lesquelles vous allez travailler")

    for (id) in database.table:
        print("Vous travaillez avec cet anésthésiste:", id)
    database.disconnect()
    
    database.connect()

    #cherche le médecin qui travaille avec l'infirmier à la date donnée et selon l'id de l'infirmier
    infirmier = ("SELECT id FROM DOCTOR WHERE id in (SELECT D_w_id from TRANSPLANTATION WHERE date = %s AND D_w_id = %s)")

    database.execute(infirmier, (date_operation, id))

    for (num) in database.table:
        print("Vous travaillez avec ces infirmiers:", num)
    
    database.disconnect()

def seedate_operations(database: DataBase, id):
    """
    According to the id of the nurse, this function allows him to see the futur dates of the transplantation he will have to make
    This function prints the different dates of his futures operations 

    Author: Eline Mota 
    
    """
    database.connect()

    dates = ("SELECT date_ FROM TRANSPLANTATION WHERE id in (SELECT id FROM N_work_on WHERE N_N_id = %s ")
    database.execute(dates, (id))

    for (date) in database.table:
        print("Vous avez des opérations à ces dates-ci:", date)
    
    database.disconnect()

def info_organe(database: DataBase):
    """
    This function allows a nurse to see the state, the way of conservation and the type of an organe by printing it 
    
    Author: Eline Mota
    
    """
    database.connect()

    id_transplantation = input("Pouvez vous me donner l'identifiant de la transplantation dont vous souhaitez voir les organes?")

    organes = ("SELECT state, method_of_preservation, type FROM ORGANE WHERE id in"
    "(SELECT Con_id FROM TRANSPLANTATION WHERE id = %s)")
    database.execute(organes, (id_transplantation))

    for (etat, methode_de_conservation, type) in database.table:
        print("voici les informations sur l'organe")
        print("Voici le type de l'organe à transplanter", type)
        print("Voici l'état de cet organe", etat)
        print("Voici la manière dont est conservé cet organe", methode_de_conservation)
    
    database.disconnect()

def info_client(database: DataBase):
    """
    This function allows a nurse to see the pseudo, the type and sign of blood of a patient on who he will have to operate.
    This function will print the pseudo, the type and signe of blood of a given patient accordinf to his id

    Authors: Eline Mota
    
    """
    client = input("Quel est l'identifiant du client dont vous souhaitez avoir les informations ? ")
    database.connect()
    clients = ("SELECT Pseudo, blood_type, blood_sign FROM CUSTOMER WHERE id in "
    "(SELECT Rec_id FROM TRANSPLANTATION WHERE Rec_id = %s")

    database.execute(clients, (client))

    for(Pseudo, type_sang, signe_sang) in database.table:
        print("voici les informations sur le client")
        print("Voici son pseudo:", Pseudo)
        print("voici son type de sang:", type_sang)
        print("Voici son signe de sang", signe_sang)