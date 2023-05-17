class UserGroupInvalidException(Exception):
    """Exception raised when an invalid user group is tried to be added to a user"""
    def __init__(self, *args, **kwargs):
        """contructor that raise the exception"""
        super().__init__(*args, **kwargs)
        