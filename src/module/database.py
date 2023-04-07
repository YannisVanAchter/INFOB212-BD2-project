# encoding uft-8
"""
Allow user of DataBase object to connect to MySQL database and execute sql inside 

Done and functionnal, check DataBase object documentation to get use example
"""
__version__ = '1.0.0'
__author__ = "Yannis Van Achter <discord:Yannis Van Achter#1444>"

import time

import mysql.connector as mysql
from mysql.connector.connection import MySQLConnection
from mysql.connector import CMySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.errors import ProgrammingError, DatabaseError

from exception.unconnectederror import UnConnectedError


class DataBase:
    """DataBase object is a collection of usefull function for database management with mysql.connector
    
    use case example:
        config = {
            "user": "user",
            "password": "password",
            "host": "mysql",
            "database": "mysql", # other config parameters
        } \n
        db = DataBase(**config) # or db = DataBase("user", "password", "mysql", "mysql")\n
        db.connect()\n
        db.execute(my_sql_querry)\n
        for row in db.table:\n
            print(row)\n
        db.disconnect()\n
    
    You can also use the with statement as follow:\n
        with DataBase(**config) as db:\n
            db.execute(my_sql_querry)\n
            for row in db.table:\n
                print(row)\n
            
    You can also use this object as parameter for execute sql querry in other functions\n
    
    For more detail about this object use print(help(DataBase))
    """

    def __init__(
        self, user: str, password: str, host: str | int, database: str, **kwargs
    ):
        """data base object initialisation

        Args:
        -----
            user (str): user name in data base
            password (str): pass word of self.user (also passed in parameters)
            host (str | int): where is the database port on network
            database (str): data base name on network
            **kwargs (dict): additional parameters for connection config
        """
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.config = kwargs
        self.__has_one_querry = False
        self.__is_connected = False
        
    def __dict__(self):
        """contain connection config 

        Returns:
            dict: config
        """
        dic = {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "database": self.database,
            "config": self.config,
        }
        return dic

    @property  # https://www.geeksforgeeks.org/python-property-decorator-property/
    def table(self) -> (list[tuple]):
        """represent the list of raws fetch from SELECT SQL command
        
        Note:
        ----- 
            replace self._DataBase__cursor.fetchall()
        """
        if self.__has_one_querry == False:
            return []
        return self.__cursor.fetchall()

    @property
    def cursor(self) -> (CMySQLCursor):
        """Get mysql.connector cursor (once connected)

        Return:
        -------
            CMySQLCursor: cursor in sql database
        """
        return self.__cursor

    @property
    def db(self) -> (MySQLConnection | CMySQLConnection):
        """get mysqle.connector connection object

        Return:
        -------
            MySQLConnection | CMySQLConnection: connection object
        """
        return self.__db

    # https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.disconnect()

    def __del__(self):
        """On delete of object disconnect from data base"""
        self.disconnect()

    def connect(self) -> (tuple[MySQLConnection | CMySQLConnection, CMySQLCursor]):
        """Connect to database and place cursor

        Raises:
        ------
            UnConnectedError: If database is not connected
            DataBaseError: If fail to connect (with more than 1000 tentative)

        Returns:
        --------
            tuple (MySQLConnection|CMySQLConnection, CMySQLCursor): db, cursor

        Version:
        --------
            1.0.0

        Authors:
        -------
            Youlan Collard & Yannis Van Achter
        """
        count_tentative = 0
        while count_tentative < 1000:
            try:
                self.__db = mysql.connect(
                    user=self.user,
                    passwd=self.password,
                    database=self.database,
                    host=self.host,
                    **self.config
                )
                if not self.__db.is_connected():
                    raise UnConnectedError()

                self.__cursor = self.__db.cursor()
                
                self.__is_connected = True

                return self.__db, self.__cursor
            except DatabaseError:
                time.sleep(0.01)
                count_tentative += 1

        raise UnConnectedError("Fail to connect to data base, please check sql container started correctly")

    def execute(self, querry: str):
        """execute SQL querry in database

        Args:
        -----
            querry (str): querry formated in SQL

        Raises:
        -------
            ProgrammingError: If SQL syntax is not correctly implemented

        Notes:
        ------
            Use self.table to get the return of the querry
        """
        origninaly_connected = True
        if not self.__is_connected:
            self.connect()
            origninaly_connected = False
            
        try:
            self.__cursor.execute(querry)
            self.__has_one_querry = True
            
            if not origninaly_connected:
                self.disconnect()
        except ProgrammingError as e:
            raise e

    def disconnect(self) -> (None):
        """Disconnect to database and close cursor

        Version:
        --------
            1.0.0

        Author:
        -------
            Youlan Collard & Yannis Van Achter
        """
        self.__cursor.close()
        self.__db.disconnect()
        self.__is_connected = False


def __init_database__():
    """Init database by insert values"""
    # with key word: https://www.geeksforgeeks.org/with-statement-in-python/
    with DataBase("user", "password", "mysql", "mysql") as db:
        # check DataBase.__enter__() method to understand why didn't I connect to database
        db.execute(
            """create table if not exists TYPE_LIVRAISON (
                    type_name varchar(16) not null,
                    price numeric(4) not null,
                    constraint ID_TYPE_LIVRAISON_ID primary key (type_name)); """
        )

        db.execute("""insert into TYPE_LIVRAISON values ('normal', 5); """)
        db.execute("""insert into TYPE_LIVRAISON values ('express', 10); """)
        db.execute("""insert into TYPE_LIVRAISON values ('internationnal', 15); """)
        db.execute("""insert into TYPE_LIVRAISON values ('main propre', 3);""")

        # for test
        # db.execute("SELECT * FROM TYPE_LIVRAISON;")

        # for row in db.table:
        #     print(row)


if __name__ == "module.database":
    # execute only if we use run file as module
    __init_database__()
