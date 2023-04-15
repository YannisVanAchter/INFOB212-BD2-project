# encoding uft-8

class UnConnectedError(Exception):
    """Exception raised when the connection to data base failled"""
    def __init__(self, *args, **kwargs):
        """contructor that raise the exception"""
        super().__init__(*args, **kwargs)
        