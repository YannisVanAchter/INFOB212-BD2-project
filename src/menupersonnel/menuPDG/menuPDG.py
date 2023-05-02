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

    print ("Do you want to add an organ?")
    organ = get_string ("Yes" or "No")
    organ_new = get_string ("which one?")
    if organ == "Yes":
        insert_into(
        database=db,
        table="ORGANE",
        attributes=("date", "id", "Con_id", "price", "Rec_id", "D_w_id", "A_w_id"),
        values=(date_choice, id, organe_id, transplantation_price, customer_id, doc_id, anesthesist_id) 
    )

    else : 
        return 0
    
