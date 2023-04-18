from module.get import *
from contants import * 

def main_persoadmin_menu (db: DataBase):
    """
    
    """

    db.connect()


    while True :
        organe_choice = get_string(print("You are there for a transplantation on which organe?", f"List of organes: {ORGAN_LIST}"))

        
        if organe_choice in ORGAN_LIST:
            print("Your selection is valid, thank you")
            break 
        
        else:
            print("Your selection is not valid, please start from the beginning idiot")
            continue

    
    date_choice = get_date(print("Enter a date for your operation"))
    print("Your operation will attend on %d", date_choice)


    print("We will assign you a doctor, an anaesthetist and a nurse")

    #Pour avoir les médecins qui sont libres
    db.execute("SELECT T.id, D_w_id, D.id FROM TRANSPLANTATION T, DOCTOR D WHERE T.D_w_id <> D.id")
    doctor_choice = db.table
    if len(doctor_choice) == 0 :
        print("All of the medecins is occuped")
    else : 
        # doctor_choice = db.execute("SELECT inami_number, D.id, T.id FROM DOCTOR D, TRANSPLANTATION T WHERE T.D_w_id <> D.id")
        doc_id = doctor_choice[0][2]
        print ("Your medecin is %i", doctor_choice)


    #Pour avoir les anathésistes qui sont libres
    db.execute("SELECT id, A_w_id FROM TRANSPLANTATION T, ANESTHESIST A WHERE T.A_w_id <> A.id")
    if len(db.table) == 0 :
        print("All of the anesthesist is occuped")
    else : 
        anesthesist_choice = db.execute("SELECT inami_number, A.id, T.id FROM TRANSPLANTATION T, ANESTHESIST A WHERE T.A_w_id <> A.id")
        print ("Your anesthesist is %i", anesthesist_choice)

    
    #Pour avoir les infirmières qui sont libres
    db.execute("SELECT T.id, NW.id, N.id FROM TRANSPLANTATION T, NURSE N, N_work_on NW WHERE N.id = NW.id and NW.id <> T.id")
    if len(db.table) == 0 :
        print("All of the nurse is occuped")
    else : 
        nurse_choice = db.execute("SELECT N.id, NW.id, N.id FROM TRANSPLANTATION T, NURSE N, N_work_on NW WHERE N.id WHERE N.id = NW.id and NW.id <> T.id")
        print ("Your nurse is %i", nurse_choice)

    #db.last_row_id
    db.execute("INSERT INTO TRANSPLANTATION (date, Con_id, price, Rec_id, D_w_id, A_w_id) ")





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
