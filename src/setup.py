
from module import DataBase

def __init():
    """Init of trigger in db"""
    import os.path as pt
    trigger_path = "../sql/triggers.sql"
    if not pt.exists(trigger_path):
        print("Trigger file not found")
    if not pt.isfile(trigger_path) and trigger_path.endswith(".sql"):
        print("Trigger file is not a SQL file")
        
    with open(trigger_path, "r") as f:
        trigger = f.read()
        with DataBase(
            host='localhost',
            user="root", 
            password="password", 
            database="db", 
            port=3306, 
            auto_connect=True
        ) as db:
            db.execute(trigger, multi=True)
       
if __name__ == "__main__":
    __init()
