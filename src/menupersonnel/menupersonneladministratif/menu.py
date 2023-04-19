from module.get import *
from constants import * 
from menupersonnel.menuaccounting.controler import *

"""
Renomer le fichier pour mieux comptendre son but, ex: menuadministrative ou mainadministrativemenu

Faire des specs pour chaque fonction.

Si une fonction du module 'get' ne fait pas exactement ce que tu veux, tu peux la modifier.
par exemple get_string(print("STING1", "STRING2" ...))
Pour que get_string supporte cette manière de recevoir les arguments, il faut modifier la fonction get_string comme suit:
def get_string(*prompt: str) -> (str):
    "SPEC"
    while True:
        try:
            return input(*prompt)
        except (TypeError, ValueError):
            pass

Faire de même pour toutes les fonctions du module 'get' qui ne font pas exactement ce que tu veux.

Le reste de la review est impossibles sans savoir (grâces aux specs) ce que tu veux faire dans cette fonction.

"""

def main_persoadmin_menu (db: DataBase):
    # TODO: SPEC FIRST !
    """
    
    """

    db.connect()


    while True :
        # if you want to pass the request to user like you do in "print"
        # you will need to update the function get_string
        organe_choice = get_string("You are there for a transplantation on which organe?", f"List of organes: {ORGAN_DICO}")

        
        if organe_choice in ORGAN_DICO:
            print("Your selection is valid, thank you")
            break 
        
        else:
            print("Your selection is not valid, please start from the beginning idiot")
            continue

    #To get the date of the operation
    date_choice = get_date("Enter a date for your operation")
    print("Your operation will attend on %d", date_choice)


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
        nurse_id = nurse_choice[0][2] # get the nurse inami from the result
        print ("Your nurse is %i", nurse_id)

    #To get the price of the organe 
    db.execute("SELECT O.price, O.type FROM ORGANE O WHERE O.type = organe_choice")

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
     
    #To get the price of the transplantation
    transplantation_price = organe_price + prix_totalblood #+ salaire 

    #Insert in the table TRANSPLANTATION
    insert_into(
        database=db,
        table="TRANSPLANTATION",
        attributes=("date", "id", "Con_id", "price", "Rec_id", "D_w_id", "A_w_id"),
        values=(date_choice, id, Con_id, transplantation_price, Rec_id, doc_id, anesthesist_id) #on ne sait pas comment remplacer Con_id et Rec_id
    )





"""
 print("Have you passed an order for a transplantation or delivery ?")
    print("Enter 1 if it is a transplantation")
    print("Enter 1 if it is a order")
    choice = get_int(print("What is your choice ?"))


    input_valid = False
    while not input_valid:
        if choice == 1:
            input_valid = True

            
        elif choice == 2:
            input_valid = True
            
            
        else:
            print("Your selection is not valid, please start from the beginning idiot")

"""
