from module.get import *
from constants import * 
from module.utils import *
from menuconnexion.menu import *

def main_persoadmin_menu (db: DataBase):
    """
    Menu for personnal administratif. 
    
    allow the personnal administratif to: 
    -------------------------------------
    - Ask for an organe, check if it is available 
    - Ask for a date, check if it is available 
    - Associate a doctor, an anesthesist, one or two nurse
    - Calculate the price of the Transplantation 
    - Insert into the table TRANPLANTATION

    Args:
        db (DataBase): Data base connected for personnal administratif 
    """

    db.connect()

    print("Welcome in the personnal administratif menu !")

    customer_id = None
    while customer_id == None:
        customer_id = get_valid_id(db, "Entrez l'id de l'utilisateur pour le quel vous voulez enregister une transplantation", "CUSTOMER")

    #Choice of the organe 
    while True :
        print("List of organes: ", ORGAN_DICO.keys())
        organe_type_choice = get_string("You are there for a transplantation on which organe?")
        if organe_type_choice in ORGAN_DICO:
            print("Your selection is valid, thank you, we will check if such an organe is available")
            break 
        else:
            print("Your selection is not valid, please start from the beginning.")
            continue
    
    #SELECT O.id, O.type, D.id, T.id FROM ORGANE O, DETAIL D, TRANSPLANTATION T WHERE O.type = %s and O.id <> D.id and O.id <> T.id", [organe_type_choice]
    #Check if such an organe is available and assiciation faire en sous requetes
    db.execute_with_params("SELECT O.id FROM ORGANE O WHERE O.type = %s and O.id not in(SELECT D.id FROM DETAIL D WHERE D.id = O.id) and O.id not in (SELECT T.Con_id FROM TRANSPLANTATION T WHERE T.Con_id = O.id);", [organe_type_choice])
    organe_choice = db.tableArgs 
    if len(organe_choice) == 0 :
        print("All of the organes of the type you have choice is occuped")
    else : 
        organe_id = organe_choice[0][0] 
        print ("Your organe is", organe_id)


    #To get the date of the operation
    if len(organe_choice) != 0 :
        while True :
            date_choice = get_date("Enter a date for your operation")
            db.execute("SELECT T.date_ FROM TRANSPLANTATION T;")
            date_table = db.table 

            if date_choice is not date_table :
                print("Your operation will attend on", date_choice)
                break

            else :
                print("Your choice is not valid, please start from the beginning idiot")
                continue
    else : 
        print("No possibilties for this organes")
            
    if len(organe_choice) != 0 :
        print("We will assign you a doctor, an anaesthetist and a or 2 nurse(s)")
        #To get the doctors who are free
        db.execute_with_params("SELECT D.inami_number, D.id FROM DOCTOR D WHERE D.id not in (SELECT T.D_w_id FROM TRANSPLANTATION T WHERE T.date_ = %s);", [date_choice])
        doctor_choice = db.tableArgs # récupère le résultat de la requête
        if len(doctor_choice) == 0 :
            print("All of the medecins is occuped")
        else : 
            doc_id = doctor_choice[0][1] # get the doc inami from the result
            print ("Your medecin is ", doctor_choice[0][0])


        #To get the anesthesists who are free
        db.execute_with_params("SELECT A.inami_number, A.id FROM ANAESTHESIST A WHERE A.id not in (SELECT T.A_w_id FROM TRANSPLANTATION T WHERE T.date_ = %s);", [date_choice])
        anesthesist_choice = db.tableArgs 
        if len(anesthesist_choice) == 0 :
            print("All of the anesthesist is occuped")
        else : 
            anesthesist_id = anesthesist_choice[0][1] # get the anesthesist inami from the result
            print ("Your anesthesist is ", anesthesist_choice[0][0])

        
        #To get the nurses who are free
        db.execute_with_params("SELECT N.id FROM NURSE N WHERE N.id not in (SELECT NW.N_N_id FROM N_work_on NW WHERE NW.id in (SELECT T.id FROM TRANSPLANTATION T WHERE T.date_ = %s));", [date_choice])
        nurse_choice = db.tableArgs 
        if len(nurse_choice) == 0 :
            print("All of the nurse is occuped")
        else : 
            nurse1_id = nurse_choice[0][0] # get the nurse id from the result
            print ("Your nurse is ", nurse1_id)
            nursenbr_choice = get_int("By default, you have one nurse, do you want a second one ? If yes, please, type 1 and 0 if one nurse is enougth for you ")
            if nursenbr_choice == 1 and len(nurse_choice) >= 2: 
                nurse2_id = nurse_choice[1][0]
                print ("Your second nurse is ", nurse2_id)
            elif nurse_choice == 1 : 
                print( "il n'y a pas d'autre nurse dispo")

        if len(doctor_choice) != 0 and len(anesthesist_choice) != 0 and len(nurse_choice) != 0 : 
            #To get the price of the price of the organe
            organe_price = ORGAN_DICO[organe_type_choice][0]

            #To get the price of the pockets of blood
            nbr_poche500 = ORGAN_DICO[organe_type_choice][1] 
            prix_500 = nbr_poche500*BLOODPOCHE
            nbr_poche480 = ORGAN_DICO[organe_type_choice][2] 
            prix_480 = nbr_poche480*BLOODPOCHE
            nbr_poche450 = ORGAN_DICO[organe_type_choice][3]
            prix_450 = nbr_poche450*BLOODPOCHE

            prix_totalblood = prix_450 + prix_480 + prix_500 

            #To get the salary of the staff
            doctor_salary = SALARY_DOCTOR_TRANSPL[organe_type_choice]
            anesthesist_salary = SALARY_ANESTHESIST_TRANSPL[organe_type_choice]
            if nursenbr_choice == 1 :
                nurse_salary = SALARY_NURSE_TRANSPL[organe_type_choice]*2
            else :
                nurse_salary = SALARY_NURSE_TRANSPL[organe_type_choice]

            salary_total = doctor_salary + anesthesist_salary + nurse_salary
            
            #To get the price of the transplantation
            transplantation_price = salary_total 

            #Check dans BLOOD
            #select les poches dispo, check si on a assez de poches pour faire la transplan (si pas assez, dire non, si oui, on garde les poches et on update les id (jointure sur details et transplantation pour verif si pas déjà pris))
            #Insert in the table TRANSPLANTATION
            insert_into(
                database=db,
                table="TRANSPLANTATION",
                attributes=("date_", "Con_id", "price", "Rec_id", "D_w_id", "A_w_id"),
                values=(date_choice, organe_id, transplantation_price, customer_id, doc_id, anesthesist_id) 
            )

        else :
            print("Unfortunately, nobody is available for your transplantation so comme back later")


#insert dans blood 

