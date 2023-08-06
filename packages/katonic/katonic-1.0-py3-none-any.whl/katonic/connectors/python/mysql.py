#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Optional
from pathlib import Path
from time import gmtime, strftime
from colorama import Fore, Style

import pandas as pd
import mysql.connector
from mysql.connector import (connection, errorcode)


class MySQLConnector:
    """Provides MySQL Connector to extracts data from mysql database."""
    _conn: Optional[connection.MySQLConnection] = None

    def __init__(
        self, 
        host: str = None, 
        port: int = 3306, 
        db_name: str = None,
        user: str = None, 
        password: str = None, 
        table_name: str = None,
        query: Optional[str] = None,
        output: Optional[str] = "local",
        file_name: Optional[str] = None,
        file_path: Optional[str] = None,
    ):
        """
        Connect with mysql database, fetch data from mysql and store into your output path.

        Args:
            host (str): database host address for eg: localhost
            port (int): connection port number (default: 3306 if not provided)
            db_name (str): database name
            user (str): mysql user name used to authenticate
            password (str): password used to authenticate
            table_name (str): table name from where you want retrieve data
            query (Optional[str]): custom query to retrieve data
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None
        """
        self._host = host
        self._port = port or 3306
        self._db_name = db_name
        self._user = user
        self._password = password
        self._table_name = table_name
        self._custom_query = query
        self._output = output
        self._file_name = file_name
        self._file_path = file_path

        if self._output.lower() == "local":
            Path(self._file_path).parent.mkdir(exist_ok=True) if self._file_path else ""
            self._dst_path = Path(self._file_path) if self._file_path else Path().absolute()
        elif self._output.lower() == "katonic":
            self._dst_path = Path("/kfs_private/")
        else:
            raise ValueError(f"invalid literal for variable output: '{self._output}', it must be one from 'local' or 'katonic'.")
        
    def _get_mysql_reg_conn(self):
        """Creates a connection to the mysql database."""
        
        if not self._conn:
            self._conn = connection.MySQLConnection(
                database=self._db_name,
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
            )

        return self._conn

    def get_data(self) -> None:
        """
        This function will extracts data from mysql database.

        Returns:
            None
        
        Raises:
            ValueError: if output type provided other than `local` or `katonic`.
        """
        fname = f"mysql_{self._db_name}_{self._file_name or self._table_name}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.csv"
        self._dst_path = str(self._dst_path / Path(fname))

        if not self._custom_query:
            self._custom_query = f"SELECT * FROM {self._db_name}.{self._table_name}"
            
        try:
            _conn = self._get_mysql_reg_conn()
            print("Connection to mysql stablished Successfully.")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            try:
                _data = pd.read_sql_query(self._custom_query, _conn)
                _data.to_csv(self._dst_path, index=False)
                print(f"File saved to your {Style.BRIGHT + Fore.GREEN}'{self._output}'{Style.RESET_ALL} file system with name {Style.BRIGHT + Fore.GREEN}'{fname}'{Style.RESET_ALL} Successfully.")
            except:
                raise ValueError(f"Failed to save data to your {Style.BRIGHT + Fore.RED}'{self._output}'{Style.RESET_ALL} file system path.")
            else:
                _conn.close()
