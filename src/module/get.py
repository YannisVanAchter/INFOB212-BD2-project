# encoding uft-8
# we could use cs50 module for it but we would need to import Falsk and other package that we won't use

def get_string(prompt: str) -> (str):
    try:
        return input(prompt)
    except EOFError:
        return None
    
def get_float(prompt: str) -> (float):
    while True:
        try:
            return float(get_string(prompt))
        except ValueError:
            pass
        
def get_int(prompt: str) -> (int):
    while True:
        try:
            return int(get_string(prompt))
        except ValueError:
            pass