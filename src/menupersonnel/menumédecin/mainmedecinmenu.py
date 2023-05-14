
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

def main_medecin_menu(database: DataBase):

    """
    Allows a medecin to navigate throughout his patients, his operations and his colleguas according to what he asks
    This function prints what the medecin has aksed for after making requests to the Database
    
    Author: Eline Mota
    """

    print("In médecin menu")
    id = int(input("Quel est votre identifiant de médecin ?")) #récupère l'identifiant du médecin

    while True:
        print("Que voulez-vous faire ?")
        print("Tapez 1 si vous voulez voir les personnes avec lesquelles vous travaillez")
        print("Tapez 2 si vous voulez voir les dates de vos futures opérations")
        print("Tapez 3 si vous voulez des informations sur un organe que vous allez transplanter")
        print("Tapez 4 si vous vouez avoir des informations sur un client en particulier")
        print("Tapez 5 ou autre chose si vous désirez arrêter de demander des informations à la base de données")

        numero = int(input("choix:"))

        if numero == 1:
            seepeople(database, id)
        
        elif numero == 2:
            seedate_operations(database, id)

        elif numero == 3:
            info_organe(database)

        elif numero == 4:
            info_client(database)
        else:
            break

def seepeople(database: DataBase, id):
    """
    Allows a medecin to see people with who he works with according to a date of an operation
    This function prints the id of the anesthesiste and nurses he works with on a certain date
    
    Author: Eline Mota
    """
    database.connect()

    idT = int(input(("Quelle est l'identifiant de la transplantation dont vous voulez voir avec qui vous allez travailler")))


    #cherche les anésthésistes qui travaillent avec le médecin à la date donnée et selon l'id du médecin
    anesthesiste = ("SELECT id, inami_number FROM ANAESTHESIST WHERE id IN (SELECT A_w_id from TRANSPLANTATION WHERE id = '%s')")

    database.execute(anesthesiste % (idT))

    print("Voici les personnes avec lesquelles vous allez travailler")

    for (ana, ina) in database.table:
        print("Vous travaillez avec cet anésthésiste:", ana, "qui a un code inami de", ina)
    database.disconnect()
    
    database.connect()

    #cherche les infirmiers qui travaillent avec le médecin à la date donnée et selon l'id du médecin 
    infirmier = ("SELECT N_N_id FROM N_work_on WHERE id IN"
    "(SELECT id FROM TRANSPLANTATION where id = '%s')")

    database.execute(infirmier% (idT))

    for (num) in database.table:
        print("Vous travaillez avec ces infirmiers:", num)
    
    database.disconnect()

def seedate_operations(database: DataBase, id):
    """
    According to the id of the medecin, this function allows him to see the futur dates of the transplantation he will have to make
    This function prints the different dates of his futures operations 

    Author: Eline Mota 
    
    """
    database.connect()

    dates = ("SELECT date_ FROM TRANSPLANTATION WHERE D_w_id = '%s' ")
    database.execute(dates % (id))

    for (date) in database.table:
        print("Vous avez des opérations à ces dates-ci:", date)
    
    database.disconnect()

def info_organe(database: DataBase):
    """
    This function allows a doctor to see the state, the way of conservation and the type of an organe by printing it 
    
    Author: Eline Mota
    
    """
    database.connect()

    id_transplantation = int(input("Pouvez vous me donner l'identifiant de la transplantation dont vous souhaitez voir les organes?"))

    organes = ("SELECT state, method_of_preservation, type FROM ORGANE WHERE id = '%s'")
    database.execute(organes % (id_transplantation))

    for (etat, methode_de_conservation, type) in database.table:
        print("voici les informations sur l'organe")
        print("Voici le type de l'organe à transplanter:", type)
        print("Voici l'état de cet organe:", etat)
        print("Voici la manière dont est conservé cet organe:", methode_de_conservation)
    
    database.disconnect()

def info_client(database: DataBase):
    """
    This function allows a doctor to see the pseudo, the type and sign of blood of a patient on who he will have to operate.
    This function will print the pseudo, the type and signe of blood of a given patient accordinf to his id

    Authors: Eline Mota
    
    """
    client = input("Quel est l'identifiant du client dont vous souhaitez avoir les informations ? ")
    database.connect()
    clients = ("SELECT Pseudo, blood_type, blood_sign FROM CUSTOMER WHERE id = '%s'")
               
    #in (SELECT Rec_id FROM TRANSPLANTATION WHERE Rec_id = '%s' ")
    
    #blood_type, blood_sign

    database.execute(clients % (client))

    for (Pseudo, type, signe) in database.table:
        print("voici les informations sur le client")
        print("Voici son pseudo:", Pseudo)
        print("voici son type de sang:", type)
        print("Voici son signe de sang", signe)

