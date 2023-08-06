#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Optional
from pathlib import Path
from io import StringIO
from time import gmtime, strftime
from colorama import Fore, Style

import pandas as pd
from azure.storage.blob import BlockBlobService


class AzureBlobConnector:
    """Provides Azure Blob Connector to extracts data from azure blob storage."""
    _blob_service: Optional[BlockBlobService] = None

    def __init__(
        self, 
        account_name: str = None, 
        account_key: str = None, 
        container_name: str = None, 
        blob_name: str = None, 
        output: Optional[str] = "local", 
        file_name: Optional[str] = None, 
        file_path: Optional[str] = None, 
    ):
        """
        Connect with azure blob database, fetch data from azure and store into your output path.

        Args:
            account_name (str): storage account name to authenticate requests signed with an account key and to construct the storage endpoint
            account_key (str): storage account key for shared key authentication
            container_name (str): name of existing container
            blob_name (str): name of existing blob
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None
        """
        self._account_name = account_name
        self._account_key = account_key
        self._container_name = container_name
        self._blob_name = blob_name
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
        
    def _get_azure_reg_conn(self):
        """Creates a connection to the azure blob."""
        
        if not self._blob_service:
            self._blob_service = BlockBlobService(account_name=self._account_name, account_key=self._account_key)

        return self._blob_service

    def get_data(self) -> None:
        """
        This function will extracts data from azure blob storage.

        Returns:
            None
        
        Raises:
            ValueError: if output type provided other than `local` or `katonic`.
        """
        fname = f"azure_{self._container_name}_{self._file_name or self._blob_name.split('.')[0]}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.csv"
        self._dst_path = str(self._dst_path / Path(fname))

        try:
            _conn = self._get_azure_reg_conn()
            print("Connection instance to azure blob storage stablished Successfully.")
        except:
            raise ValueError("Connection to azure blob storage failed.")
        else:
            try:
                _data_string = _conn.get_blob_to_text(self._container_name, self._blob_name, encoding="latin1").content
                _data = pd.read_csv(StringIO(_data_string))

                _data.to_csv(self._dst_path, index=False)
                print(f"File saved to your {Style.BRIGHT + Fore.GREEN}'{self._output}'{Style.RESET_ALL} file system with name {Style.BRIGHT + Fore.GREEN}'{fname}'{Style.RESET_ALL} Successfully.")
            except:
                raise ValueError(f"Failed to save data to your {Style.BRIGHT + Fore.RED}'{self._output}'{Style.RESET_ALL} file system path.")
