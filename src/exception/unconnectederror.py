# encoding uft-8

class UnConnectedError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        