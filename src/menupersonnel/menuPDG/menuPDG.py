from module.get import *
from constants import * 
from module.utils import *
from menuconnexion.menu import *
from menupersonnel.menuaccounting.mainaccountingmenu import *
from menupersonnel.menumédecin.mainmedecinmenu import *
from menupersonnel.menumédecin.mainmenuanesthesiste import *
from menupersonnel.menumédecin.menuinfirmier import *
from menupersonnel.menupersonneladministratif import *
from menupersonnel.RH import *
from module.database import *

def PDG_menu ():
    """
    """
    print ("Do you want to acces to the accountant menu?")
    want_accounting = get_string ("Yes" or "No")
    if want_accounting == "Yes":
        main_accounting_menu()
    else : 
        return 0 
    
    print ("Do you want to acces to the medecin menu?")
    want_sexydoctor = get_string ("Yes" or "No")
    if want_sexydoctor == "Yes":
        main_medecin_menu()
    else : 
        return 0 
    
    print ("Do you want to acces to the medecin menu?")
    want_anesthechit = get_string ("Yes" or "No")
    if want_anesthechit == "Yes":
        main_anesthesiste_menu()
    else : 
        return 0 
    
    print ("Do you want to acces to the medecin menu?")
    want_uglynurse = get_string ("Yes" or "No")
    if want_uglynurse == "Yes":
        main_infirmier_menu()
    else : 
        return 0 
    
    print ("Do you want to acces to the administratif menu?")
    want_administratif = get_string ("Yes" or "No")
    if want_administratif == "Yes":
        main_persoadmin_menu ()
    else : 
        return 0 

    print ("Do you want to acces to the RH menu?")
    want_RH = get_string ("Yes" or "No")
    if want_RH == "Yes":
        main_RH_menu ()
    else : 
        return 0 
    
    print ("Do you want to delete this PDG?")
    delete_PDG = get_string ("Yes" or "No")
    if delete_PDG == "Yes":
        suppression_PDG ()
    else : 
        return 0
    
    print ("Do you want to insert a new element?")
    insert_elt = get_string ("Yes" or "No")
    if insert_elt == "Yes":
        insert_newelements ()
    else : 
        return 0 
    
def suppression_PDG (db : DataBase, user_id):
    """
    Menu to delete a PDG. 
    
    allow the PDG to: 
    -------------------------------------
    - 

    Args:
        db (DataBase): Data base connected for personnal administratif 
        user_id : the id of the pdg qu'on veut supp  et qui est connecté

    """
    db.connect

    db.delete ("SELECT C.id, S.id FROM CEO C, STAFF S WHERE C.id = S.id and C.id = user_id")

def insert_newelements (db : DataBase):
    """
    """
    db.connect

    #Insert a new organ
    print ("Do you want to add an organ?")
    organ = get_string ("Yes" or "No")
    organ_new = get_string ("which one?")
    organ_new_price = get_float("What is its price, in float ?") 
    organ_new_state = get_string("What is the state of this new organ ? Very good, good, average, poor or very poor ?")#voir si avec menu médecin ?
    organ_new_functionnal = get_string ("This new organ is functionnal, Yes or No ?")
    organ_new_expiration_date = get_date ("What is the expiration date of this organ ?") #menu medecin aussi ?
    organ_new_expiration_date_tranplantation =  get_date("Enter the date of today") +  get_date("Enter the date of today + 5 months")
    db.table = db.execute("SELECT O.id, D.id, O.type FROM ORGAN O, DONATOR D WHERE O.id = D.id and O.type = organ_new")
    Donator_id = db.table[0][1]
    organ_new_method_of_preservation = get_string("What is the method of preservation of this new organ ? For example : In the fridge under -10 degrees ")
    if organ == "Yes":
        insert_into(
        database=db,
        table="ORGANE",
        attributes=("state", "functionnal", "expiration_date", "expiration_date_transplantation", "method_of_preservation", "type", "id", "price", "Com_id"),
        values= (organ_new_state, organ_new_functionnal, organ_new_expiration_date, organ_new_expiration_date_tranplantation, organ_new_method_of_preservation,organ_new, id, organ_new_price, Donator_id)
    )

    else : 
        return 0
    
    #Insert a new type of delivery 
    print ("Do you want to add a new type of delivery ?")
    tp_delivery = get_string ("Yes" or "No")
    tp_delivery_id = get_string ("which one?")
    organ_new_price = get_float("What is its price?") 
    if tp_delivery == "Yes":
        insert_into(
        database=db,
        table="TYPE_DELIVERY",
        attributes=("id", "price"),
        values= (tp_delivery_id, organ_new_price)
    )

    else : 
        return 0
