import os
from typing import Union

from .common import build_connection_string
from ..common.env import (
    IMBALANCE_DATA_DATABASE,
    IMBALANCE_DATA_ASSIGNED_UID,
    IMBALANCE_DATA_PASSWORD,
    IMBALANCE_DATA_PROTOCOL,
    IMBALANCE_DATA_SERVER,
    IMBALANCE_DATA_USERNAME
)
from ..common import mienums

def get_connection_string(
    server_var: str=IMBALANCE_DATA_SERVER,
    server_override: Union[str, None] = None,
    database_var: str=IMBALANCE_DATA_DATABASE,
    database_override: Union[str, None] = None,
    protocol_var: str=IMBALANCE_DATA_PROTOCOL,
    protocol_override: Union[str, None] = None,
    username_var: str=IMBALANCE_DATA_USERNAME,
    username_override: Union[str, None] = None,
    password_var: str=IMBALANCE_DATA_PASSWORD,
    password_override: Union[str, None] = None,
    msi_uid_var: str=IMBALANCE_DATA_ASSIGNED_UID,
    msi_uid_override: Union[str, None] = None,
    driver_override: Union[str, None] = None,
    platform_override: Union[str, mienums.OsPlatform, None] = None):
    
    # Get the server property
    if server_override is not None:
        server = server_override
    else:
        server = os.environ.get(server_var, None)
    
    if server is None:
        raise EnvironmentError('Server has not been provided')

    # Get the database property
    if database_override is not None:
        database = database_override
    else:
        database = os.environ.get(database_var, None)
    
    if database is None:
        raise EnvironmentError('Database has not been provided')

    # Get the protocol property
    if protocol_override is not None:
        protocol = protocol_override
    else:
        protocol = os.environ.get(protocol_var, None)

    # Get the username property
    if username_override is not None:
        username = username_override
    else:
        username = os.environ.get(username_var, None)

    # Get the password property
    if password_override is not None:
        password = password_override
    else:
        password = os.environ.get(password_var, None)

    # Get the uid property
    if msi_uid_override is not None:
        msi_uid = msi_uid_override
    else:
        msi_uid = os.environ.get(msi_uid_var, None)
    
    # Build the connection string
    connection_string = build_connection_string(
        server=server,
        database=database,
        protocol=protocol,
        username=username,
        password=password,
        msi_uid=msi_uid,
        driver=driver_override,
        use_platform=platform_override
    )

    # Return the connection string
    return connection_string