# encoding uft-8

import os


def clear_terminal():
    """clear terminal"""
    command = 'clear'
    if os.name in ('nt', 'dos'): # Windows
        command = 'cls'
    os.system(command)
