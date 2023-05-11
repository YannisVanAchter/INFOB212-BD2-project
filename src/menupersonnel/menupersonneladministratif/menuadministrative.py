from module.get import *
from constants import * 
from module.utils import *
from menuconnexion.menu import *

def main_persoadmin_menu (db: DataBase, customer_id):
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
        customer_id : the id of the connected customer 
    """

    db.connect()


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

    #Check if such an organe is available and assiciation 
    db.execute(f"SELECT O.id, O.type, D.id, T.id FROM ORGANE O, DETAIL D, TRANSPLANTATION T WHERE O.type = '{organe_type_choice}' and O.id <> D.id and O.id <> T.id")
    organe_choice = db.table 
    if len(organe_choice) == 0 :
        print("All of the organes of the type you have choice is occuped")
    else : 
        organe_id = organe_choice[0][0] 
        print ("Your organe is %i", organe_id)


    #To get the date of the operation
    if len(organe_choice) != 0 :
        while True :
            date_choice = get_date("Enter a date for your operation")
            db.execute("SELECT T.date FROM TRANPLANTATION T")
            date_table = db.table 

            if date_choice is not date_table :
                print("Your operation will attend on %d", date_choice)
                break

            else :
                print("Your choice is not valid, please start from the beginning idiot")
                continue
    else : 
        print("No possibilties for this organes")
            
    if len(organe_choice) != 0 :
        print("We will assign you a doctor, an anaesthetist and a nurse")
        #To get the doctors who are free
        db.execute("SELECT T.id, D.inami_number, D.D_w_id, D.id FROM TRANSPLANTATION T, DOCTOR D WHERE T.D_w_id <> D.id")
        doctor_choice = db.table # récupère le résultat de la requête
        if len(doctor_choice) == 0 :
            print("All of the medecins is occuped")
        else : 
            doc_id = doctor_choice[0][3] # get the doc inami from the result
            print ("Your medecin is %i", doc_id)


        #To get the anesthesists who are free
        db.execute("SELECT T.id, T.A_w_id, A.inami_number, A.id FROM TRANSPLANTATION T, ANESTHESIST A WHERE T.A_w_id <> A.id")
        anesthesist_choice = db.table 
        if len(anesthesist_choice) == 0 :
            print("All of the anesthesist is occuped")
        else : 
            anesthesist_id = anesthesist_choice[0][3] # get the anesthesist inami from the result
            print ("Your anesthesist is %i", anesthesist_id)

        
        #To get the nurses who are free
        db.execute("SELECT T.id, NW.id, N.id FROM TRANSPLANTATION T, NURSE N, N_work_on NW WHERE N.id = NW.id and NW.id <> T.id")
        nurse_choice = db.table 
        if len(nurse_choice) == 0 :
            print("All of the nurse is occuped")
        else : 
            nurse1_id = nurse_choice[0][2] # get the nurse inami from the result
            print ("Your nurse is %i", nurse1_id)
            nursenbr_choice = print ("By default, you have one nurse, do you want a second one ? If yes, please, type 1 and 0 if one nurse is enougth for you")
            if nursenbr_choice == 1 : 
                nurse2_id = nurse_choice[1][2]
                print ("Your nurse is %i", nurse2_id)


        #To get the price of the price of the organe
        organe_price = ORGAN_DICO[organe_choice][0]

        #To get the price of the pockets of blood
        nbr_poche500 = ORGAN_DICO[organe_choice][1] 
        prix_500 = nbr_poche500*BLOODPOCHE
        nbr_poche480 = ORGAN_DICO[organe_choice][2] 
        prix_480 = nbr_poche480*BLOODPOCHE
        nbr_poche450 = ORGAN_DICO[organe_choice][3]
        prix_450 = nbr_poche450*BLOODPOCHE

        prix_totalblood = prix_450 + prix_480 + prix_500 

        #To get the salary of the staff
        doctor_salary = SALARY_DOCTOR_TRANSPL[organe_choice]
        anesthesist_salary = SALARY_ANESTHESIST_TRANSPL[organe_choice]
        if nursenbr_choice == 1 :
            nurse_salary = SALARY_NURSE_TRANSPL[organe_choice]*2
        else :
            nurse_salary = SALARY_NURSE_TRANSPL[organe_choice]

        salary_total = doctor_salary + anesthesist_salary + nurse_salary
        
        #To get the price of the transplantation
        transplantation_price = organe_price + prix_totalblood + salary_total 

        #Insert in the table TRANSPLANTATION
        insert_into(
            database=db,
            table="TRANSPLANTATION",
            attributes=("date_", "id", "Con_id", "price", "Rec_id", "D_w_id", "A_w_id"),
            values=(date_choice, id, organe_id, transplantation_price, customer_id, doc_id, anesthesist_id) 
        )


