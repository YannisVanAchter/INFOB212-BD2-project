# encoding uft-8

import time

import mysql.connector as mysql
from mysql.connector.connection import MySQLConnection
from mysql.connector import CMySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor
from mysql.connector.errors import ProgrammingError, DatabaseError

from exception.unconnectederror import UnConnectedError


class DataBase:
    """DataBase object is a collection of usefull function for database management with mysql.connector"""

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

    @property
    def table(self) -> (list[tuple]):
        """represent the list of raws fetch from SELECT SQL command"""
        if self.__has_one_querry == False:
            return []
        return self.__cursor.fetchall()

    @table.setter
    def table(self, *value) -> (Exception()):
        """represent the list of raws fetch from SELECT SQL command"""
        raise ValueError(
            "You can not set value in database table like it, use self.execute(...) to run sql command for insert, delete, create or update."
        )

    @property
    def cursor(self):
        return self.__cursor

    @property
    def db(self):
        return self.__db

    def connect(self) -> (tuple[MySQLConnection | CMySQLConnection, CMySQLCursor]):
        """Connect to database and place cursor

        Raises:
        ------
            UnConnectedError: If database is not connected
            DataBaseError: If fail to connect (with more than 300 tentative)

        Returns:
        --------
            tuple (MySQLConnection|CMySQLConnection, CMySQLCursor): db, cursor

        Version:
        --------
            1.0.0

        Author:
        -------
            Youlan Collart & Yannis Van Achter
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

                return self.__db, self.__cursor
            except DatabaseError as e:
                time.sleep(0.01)
                count_tentative += 1

        raise e

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
        try:
            self.__cursor.execute(querry)
            self.__has_one_querry = True
        except ProgrammingError as e:
            raise e

    def disconnect(self) -> (None):
        """Disconnect to database and close cursor

        Version:
        --------
            1.0.0

        Author:
        -------
            Youlan Collart & Yannis Van Achter
        """
        self.__cursor.close()
        self.__db.disconnect()
