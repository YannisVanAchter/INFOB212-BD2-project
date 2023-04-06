# encoding uft-8

import os


def clear_terminal(command="clear"):
    """clear terminal
    
    args:
    -----
        command (str): Bash command set for Linux/MacOS operating system by default. Set string to "cls" for windows
    """
    os.system(command)
