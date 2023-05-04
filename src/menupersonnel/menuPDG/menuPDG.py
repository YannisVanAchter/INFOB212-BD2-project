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

    #Insert a new organ verif que c'est pas dedans 
    print ("Do you want to add an organ?")
    organ = get_string ("Yes" or "No")
    organ_new = get_string ("which one?")
    organ_new_price = get_float("What is the price of your new organ ?")
    organ_500ML = get_int("How much blood bag of 500 ml do we need for a transplantation of this new organ ? It could be 0")
    organ_480ML = get_int("How much blood bag of 480 ml do we need for a transplantation of this new organ ? It could be 0")
    organ_450ML = get_int("How much blood bag of 450 ml do we need for a transplantation of this new organ ? It could be 0")

    if organ_new not in ORGAN_DICO :
        ORGAN_DICO.update({organ_new : [organ_new_price, organ_500ML, organ_480ML, organ_450ML]})
        insert_organ()
    else : 
        print("This type of organ already exist ;)s")

    #Insert a new type of delivery TODO
    print ("Do you want to add a new type of delivery ?")
    tp_delivery = get_string ("Yes" or "No")
    tp_delivery_id = get_string ("which one?")
    tp_delivery_new_price = get_float("What is its price?") 
    if tp_delivery == "Yes":
        insert_into(
        database=db,
        table="TYPE_DELIVERY",
        attributes=("id", "price"),
        values= (tp_delivery_id, tp_delivery_new_price)
    )

    else : 
        return 0
