import time # remove unused import
import datetime
import mysql.connector as mysql

from module.database import DataBase

def main_medecin_menu(database: DataBase):
    # connection is not requere, Youlan manage it 
    print("In médecin menu")
    id = str(input("Quel est votre identifiant de médecin ?")) #récupère l'identifiant du médecin
    
    # keep code bellow
    print("Que voulez-vous faire ?")
    print("Tapez 1 si vous voulez voir les personnes avec lesquelles vous travaillez")
    print("Tapez 2 si vous voulez voir les dates de vos futures opérations")
    print("Tapez 3 si vous voulez des informations sur un organe que vous allez transplanter")
    print("Tapez 4 si vous vouez avoir des informations sur un client en particulier")
    # you can use this command and use function linked 'from module.get import get_int' to this line use: numero = get_int("choix:")
    numero = int(input("choix:"))

    if numero == 1:
        # you imported "mysql.connector as mysql" use "mysql" key word to acces to connector
        # you can also replace those line by call "database.connect()" and use "database.execute(YOUR_QUERRY)"
        cnx = mysql.connect(user='UserMedecin', database= DataBase ) #jsp comment faire cette partie, HELP
        cursor = cnx.cursor()


        print("Quelle est la date de l'opération dont vous voulez voir les personnes avec qui vous allez travailler ? ")
        annee = int(input("Donnez moi l'année de l'opération"))
        jour = int(input("Donnez moi le jour de l'opération"))
        mois = int(input("Donnez moi le mois de l'opération"))

        #transforme en date
        date_operation = datetime.date(annee, jour, mois)

        #cherche les anésthésistes qui travaillent avec le médecin à la date donnée et selon l'id du médecin
        anesthésiste = ("SELECT id FROM ANESTHESISTE WHERE num in (SELECT A_t_id from TRANSPLANTATION WHERE date = %s AND id = %s)")

        # you can use database.execute(...)
        cursor.execute(anesthésiste, (date_operation, id))

        print("Voici les personnes avec lesquelles vous allez travailler")
        # to get result use cursor.fetchall()
        # you can also use "database.table" 
        for (id) in cursor:
            print("Vous travaillez avec cet anésthésiste:", id)
        cursor.close()
        cnx.close()
        
        cnx = mysql.connect(user='UserMedecin', database= DataBase ) #jsp comment faire cette partie, HELP
        cursor = cnx.cursor()

        #cherche les infirmiers qui travaillent avec le médecin à la date donnée et selon l'id du médecin 
        infirmier = ("SELECT num FROM INFIRMIER WHERE num in (SELECT num FROM I_travail_sur WHERE id_transplantation in"
        "(SELECT id_transplantation FROM TRANSPLANTATION where date = %s AND id = %s))")
        cursor.execute(infirmier, (date_operation, id))

        for (num) in cursor:
            print("Vous travaillez avec ces infirmiers:", num)
        
        cursor.close()
        cnx.close()
    
    elif numero == 2:
        cnx = mysql.connect(user='UserMedecin', database= DataBase ) #jsp comment faire cette partie, HELP
        cursor = cnx.cursor()

        dates = ("SELECT date FROM TRANSPLANTATION WHERE id = %s ")
        cursor.execute(infirmier, (id))

        for (date) in cursor:
            print("Vous avez des opérations à ces dates-ci:", date)
        
        cursor.close()
        cnx.close()

    elif numero == 3:
        cnx = mysql.connect(user='UserMedecin', database= DataBase ) #jsp comment faire cette partie, HELP
        cursor = cnx.cursor()

        id_transplantation = input("Pouvez vous me donner l'identifiant de la transplantation dont vous souhaitez voir les organes?")

        # use 3*" your querry 3*", that will provide only one string
        #
        # Example:
        # organes = ("""SELECT etat, methode_de_conservation, type FROM ORGANE WHERE id_organe in
        # (SELECT id_organe FROM TRANSPLANTATION WHERE id_transplantation = %s)""")
        organes = ("SELECT etat, methode_de_conservation, type FROM ORGANE WHERE id_organe in"
        "(SELECT id_organe FROM TRANSPLANTATION WHERE id_transplantation = %s)")
        cursor.execute(organes, (id_transplantation))

        for (etat, methode_de_conservation, type) in cursor:
            print("voici les informations sur l'organe")
            print("Voici le type de l'organe à transplanter", type)
            print("Voici l'état de cet organe", etat)
            print("Voici la manière dont est conservé cet organe", methode_de_conservation)
        
        cursor.close()
        cnx.close()


    elif numero == 4:
        client = input("Quel est l'identifiant du client dont vous souhaitez avoir les informations ? ")
        cnx = mysql.connect(user='UserMedecin', database= DataBase ) #jsp comment faire cette partie, HELP
        cursor = cnx.cursor()

        clients = ("SELECT Pseudo, type_sang, signe_sang FROM CLIENT WHERE id in "
        "(SELECT Rec_id FROM TRANSPLANTATION WHERE Rec_id %s")

        cursor.execute(clients, (client))

        for(Pseudo, type_sang, signe_sang) in cursor:
            print("voici les informations sur le client")
            print("Voici son pseudo:", Pseudo)
            print("voici son type de sang:", type_sang)
            print("Voici son signe de dans", signe_sang)

    else:
        print("Error")


