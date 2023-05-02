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
        main_RH_menu()
    else : 
        return 0 
    
    print ("Do you want to delete this PDG?")
    delete_PDG = get_string ("Yes" or "No")
    if delete_PDG == "Yes":
        suppression_PDG ()
    else : 
        return 0
    
def suppression_PDG (db : DataBase, user_id):
    """
    Menu to delete a PDG. 
    
    allow the PDG to: 
    -------------------------------------
    - Ask for an organe, check if it is available 
    - Ask for a date, check if it is available 
    - Associate a doctor, an anesthesist, one or two nurse
    - Calculate the price of the Transplantation 
    - Insert into the table TRANPLANTATION

    Args:
        db (DataBase): Data base connected for personnal administratif 
        user_id : the id of the connected customer 

    """

    

 


    






    

