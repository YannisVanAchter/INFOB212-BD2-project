# encoding uft-8
"""
Allow user of DataBase object to connect to MySQL database and execute sql inside 

Follow the pep 249 functionnality for more information about the functionnality of this object 
follow this link: https://peps.python.org/pep-0249/

Done and functionnal, check DataBase object documentation to get examples of use
"""
__version__ = "1.1.0"
__author__  = "Yannis Van Achter <discord:Yannis Van Achter#1444>"

import time

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import ProgrammingError, DatabaseError

from exception.unconnectederror import UnConnectedError


class DataBase:
    """DataBase object is a collection of useful function for database management with mysql.connector

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

    You can also use this object as parameter to execute sql querry in other functions\n

    For more details about this object use print(help(DataBase))
    """

    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        database: str,
        port: int,
        auto_connect: bool = False,
        # auto_commit: bool = False,
        **kwargs
    ):
        """data base object initialisation

        Args:
        -----
            user (str): user name in data base
            password (str): pass word of self.user (also passed in parameters)
            host (str): where is the database port on network
            database (str): data base name on network
            port (int): port of database (3306 by default in mysql docker server)
            auto_connect (bool): if True connect to database on initialisation and before each querry. Default to False
            auto_commit (bool): if True commit to database after each querry. Default to False
            **kwargs (dict): additional parameters for connection config
        """
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.config = kwargs
        self.__has_one_querry = False
        self.__is_connected = False
        self.auto_connect = auto_connect
        self.__fetched = []
        self.__fetchedPrepared = []
        self.__cursor = None
        self.__db = None

        if auto_connect:
            self.connect()

    def __dict__(self) -> (dict):
        """contain connection config

        Returns:
            dict: config
        """
        dic = {
            "user": self.user,
            "password": self.password,
            "host": self.host,
            "database": self.database,
            "port": self.port,
            "config": self.config,
        }
        return dic

    # https://www.geeksforgeeks.org/python-property-decorator-property/
    @property  
    def table(self) -> (list[tuple]):
        """represent the list of raws fetch from SELECT SQL command

        Note:
        -----
            replace self._DataBase__cursor.fetchall()
        """
        return self.__fetched
    
    @property
    def tableArgs(self) -> (list[tuple]):
        """Represent the list of raws fetch from SELECT SQL command when args are used
        
        """
        return self.__fetchedPrepared

    @property
    def cursor(self) -> (MySQLCursor):
        """Get mysql.connector cursor (once connected)

        Return:
        -------
            MySQLCursor: cursor in sql database
        """
        if self.auto_connect:
            self.connect()
        return self.__cursor

    @property
    def db(self) -> (MySQLConnection):
        """get mysqle.connector connection object

        Return:
        -------
            MySQLConnection | CMySQLConnection: connection object
        """
        if self.auto_connect:
            self.connect()
        return self.__db

    @property
    def last_row_id(self):
        """Returns id of the last row inserted"""
        return self.__cursor.lastrowid
    
    @property
    def last_row_id_with_params(self):
        return self.__cursorPrepared.lastrowid

    # https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    def __enter__(self):
        """Enter method for with statement"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, trace):
        """Exit method for with statement"""
        self.disconnect()

    def __del__(self):
        """On delete of object disconnect from data base"""
        if self.__is_connected:
            self.disconnect()

    def connect(self) -> (tuple[MySQLConnection, MySQLCursor]):
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
        e = None
        while count_tentative < 1000:
            try:
                self.__db = connect(
                    user=self.user,
                    passwd=self.password,
                    database=self.database,
                    host=self.host,
                    port=self.port,
                    connect_timeout=999999,
                    **self.config
                )
                if not self.__db.is_connected():
                    raise UnConnectedError()

                self.__cursor = self.__db.cursor(buffered=True)
                self.__cursorPrepared = self.__db.cursor(prepared=True)

                self.__is_connected = True

                return self.__db, self.__cursor
            
            except DatabaseError as err:
                time.sleep(0.01)
                count_tentative += 1
                e = err

        raise UnConnectedError(
            "Fail to connect to data base, please check sql container started correctly \n"
            + f"Original error: {type(e)} {e}"
        )

    def execute(self, querry: str, multi: bool = False):
        """execute SQL querry in database

        Args:
        -----
            querry (str): querry formated in SQL

        Raises:
        -------
            ProgrammingError: If SQL syntax is not correctly implemented

        Notes:
        ------
            Make sure to be connected to the database before execute querry
            Use self.table to get the return of the querry
        """
        if self.auto_connect and not self.__is_connected:
            self.connect()
            
        if not self.__is_connected:
            raise UnConnectedError(
                "you must be connected to database before execute querry"
            )
            
        querry = querry.strip()
        try:
            # create new cursor before next query to keep acces to last query
            self.__cursor.close()
            self.__cursor = self.__db.cursor()
            if multi:
                for _ in self.__cursor.execute(querry, multi=multi):
                    pass
                if not self.__db.is_connected():
                    self.__db.reconnect()

            else:
                self.__cursor.execute(querry, multi=multi)
                if (
                    querry.strip().upper().startswith("SELECT")
                    or querry.strip().upper().startswith("SHOW")
                ):
                    self.__fetched = self.__cursor.fetchall()
                    if (not self.__db.is_connected()):
                        self.__db.reconnect()
                    self.__cursor.nextset()
                elif (not self.__db.is_connected()):
                    self.__db.reconnect()
        except ProgrammingError as e:
            raise e
        finally:
            if self.auto_connect and not self.__is_connected:
                self.disconnect()
                pass

    def execute_with_params(self, query: str, argsTuple: tuple) -> (int):
        """Execute a query and returns its id if an insert was made. -1 otherwise.
        """
        toReturn = -1
        self.__cursorPrepared.execute(query, argsTuple)
        print(self.__cursorPrepared)
        if self.__cursorPrepared.with_rows:
            self.__fetchedPrepared = self.__cursorPrepared.fetchall()
            if (not self.__db.is_connected()):
                self.__db.recconect()
            self.__cursorPrepared.nextset()
        else:
            if (not self.__db.is_connected()):
                self.__db.recconect()
            if query.startswith("INSERT") or query.startswith("UPDATE"):
                toReturn = self.__cursorPrepared.lastrowid
                self.__db.commit()
            self.__cursorPrepared.close()
            self.__cursorPrepared = self.__db.cursor(prepared=True)
        return toReturn


    def execute_many(self, *querry: str):
        """execute many SQL querry in database

        Args:
        -----
            querry (str): querry formated in SQL

        Raises:
        -------
            ProgrammingError: If SQL syntax is not correctly implemented

        Notes:
        ------
            Make sure to be connected to the database before execute querry
            Use self.table to get the return of the querry
        """
        multi_select = []
        for q in querry:
            self.execute(q)
            if q.upper().startswith("SELECT"):
                multi_select.append(self.table)
        return multi_select

    def disconnect(self) -> (None):
        """Disconnect to database and close cursor

        Version:
        --------
            1.0.0

        Author:
        -------
            Youlan Collard & Yannis Van Achter
        """
        self.__db.close()
        self.__is_connected = False
