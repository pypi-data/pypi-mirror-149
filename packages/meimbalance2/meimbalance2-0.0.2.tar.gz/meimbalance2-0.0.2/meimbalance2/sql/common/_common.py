import logging
import platform
import pyodbc
import logging

from typing import Union

from ...common.mienums import OsPlatform, SqlProtocol

_logger = logging.getLogger(__name__)

def build_connection_string(
    server: str, database: str, driver: Union[str, None]=None,
    use_platform: Union[OsPlatform, None]=None, protocol: Union[str, SqlProtocol, None] = None,
    username: Union[str, None] = None, password: Union[str, None] = None,
    msi_uid: Union[str, None] = None) -> str:
    """TODO: Add description
    """

    # Allow for driver override
    if driver is None:
        driver='ODBC Driver 17 for SQL Server'
        if (use_platform is None and platform.system() == 'Windows') or str(use_platform) == str(OsPlatform.windows):
            driver='SQL Server' 

    # Set the basic connection string
    connection_string = 'DRIVER={' + driver + '};SERVER=' + server + ';DATABASE=' + database

    # Set the protocol specific syntax
    if str(protocol) not in [str(SqlProtocol.integrated), str(SqlProtocol.interactive), str(SqlProtocol.msi)]:

        # Verify that username and password has been provided
        if username is None or password is None:
            raise ValueError('username and password must be given for non-ActiveDirectory workloads.')
        
        # Update connection string
        connection_string += ';UID=' + username + ';PWD=' + password
    else:
        connection_string += ';Authentication=' + str(protocol)

        # set uid if provided for msi (user assigned identity)
        if str(protocol) == str(SqlProtocol.msi) and msi_uid is not None:
            connection_string += ';UID=' + msi_uid
    return connection_string


def get_connection(connection_string: str) -> pyodbc.Connection:
    connection = None
    for i in range(5):
        try:
            connection = pyodbc.connect(connstring=connection_string)
            break
        except:
            _logger.info(f'Connection attempt {i} failed, retrying')
    
    if connection is None:
        raise ConnectionError('Unable to establish a connection')

