#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Optional
from pathlib import Path
from time import gmtime, strftime
from colorama import Fore, Style

import snowflake.connector


class SnowFlakeConnector:
    """Provides Snowflake Connector to extracts data from snowflake database."""
    _conn: Optional[snowflake.connector.connect] = None

    def __init__(
        self, 
        user: str, 
        password: str, 
        account: str, 
        database: str,
        table_name: str,
        schema: str,
        warehouse: str = None, 
        query: Optional[str] = None,
        output: Optional[str] = "local",
        file_name: Optional[str] = None,
        file_path: Optional[str] = None,
    ):
        """
        Connect with snowflake, fetch data from snowflake and store into your output path.

        Args:
            user (str): login name for the user to authenticate
            password (str): password for the user to authenticate
            account (str): your account identifier
            database (str): name of the default database to use
            table_name (str): table name from where you want retrieve data
            schema (str): name of the default schema to use for the database
            warehouse (int): name of the default warehouse to use
            query (Optional[str]): custom query to retrieve data
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None
        """
        self._user = user
        self._password = password
        self._account = account
        self._warehouse = warehouse
        self._database = database
        self._table_name = table_name
        self._schema = schema
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
        
    def _get_snowflake_reg_conn(self):
        """Creates a connection to the snowflake database."""

        if not self._conn:

            self._conn = snowflake.connector.connect(
                user=self._user,
                password=self._password,
                account=self._account,
            )

        return self._conn

    def get_data(self) -> None:
        """
        This function will extracts data from snowflake database.

        Returns:
            None
        
        Raises:
            ValueError: if output type provided other than `local` or `katonic`.
        """

        fname = f"snowflake_{self._schema}_{self._database}_{self._file_name or self._table_name}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.csv"
        self._dst_path = str(self._dst_path / Path(fname))

        if not self._custom_query:
            self._custom_query = f"SELECT * FROM {self._schema}.{self._table_name};"
            
        try:
            _conn = self._get_snowflake_reg_conn()
            _cur = _conn.cursor()

            if self._warehouse:
                try:
                    _cur.execute(f"USE WAREHOUSE {self._warehouse}")
                except snowflake.connector.errors.ProgrammingError as e:
                    print(e)

            if self._database:
                try:
                    _cur.execute(f"USE DATABASE {self._database}")
                except snowflake.connector.errors.ProgrammingError as e:
                    print(e)
                
            if self._schema:
                try:
                    _cur.execute(f"USE SCHEMA {self._schema}")
                except snowflake.connector.errors.ProgrammingError as e:
                    print(e)
            
            print("Connection to snowflake stablished Successfully.")
        
        except snowflake.connector.errors.ProgrammingError as e:
            print(f'Error {e.errno} ({e.sqlstate}): {e.msg} ({e.sfqid})')
        else:
            try:
                try:
                    _cur.execute(self._custom_query)
                except snowflake.connector.errors.ProgrammingError as e:
                    print(e)
                else:
                    # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
                    _data = _cur.fetch_pandas_all()
                    _data.to_csv(self._dst_path, index=False)
                    print(f"File saved to your {Style.BRIGHT + Fore.GREEN}'{self._output}'{Style.RESET_ALL} file system with name {Style.BRIGHT + Fore.GREEN}'{fname}'{Style.RESET_ALL} Successfully.")
            except:
                raise ValueError(f"Failed to save data to your {Style.BRIGHT + Fore.RED}'{self._output}'{Style.RESET_ALL} file system path.")
            finally:
                _cur.close()
                _conn.close()
