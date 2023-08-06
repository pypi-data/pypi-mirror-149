import os
from typing import Union
from datetime import datetime
from datetime import timezone

from .common import build_connection_string, get_connection
from ..common.env import (
    IMBALANCE_LOG_DATABASE,
    IMBALANCE_LOG_ASSIGNED_UID,
    IMBALANCE_LOG_PASSWORD,
    IMBALANCE_LOG_PROTOCOL,
    IMBALANCE_LOG_SERVER,
    IMBALANCE_LOG_USERNAME
)
from ..common import mienums

def get_connection_string(
    server_var: str=IMBALANCE_LOG_SERVER,
    server_override: Union[str, None] = None,
    database_var: str=IMBALANCE_LOG_DATABASE,
    database_override: Union[str, None] = None,
    protocol_var: str=IMBALANCE_LOG_PROTOCOL,
    protocol_override: Union[str, None] = None,
    username_var: str=IMBALANCE_LOG_USERNAME,
    username_override: Union[str, None] = None,
    password_var: str=IMBALANCE_LOG_PASSWORD,
    password_override: Union[str, None] = None,
    msi_uid_var: str=IMBALANCE_LOG_ASSIGNED_UID,
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

def log_files(filetype, filename, url, status, message):
    now = datetime.now(tz=timezone.utc)
    connection_string = get_connection_string()
    connection = get_connection(connection_string=connection_string)
    cursor = connection.cursor()
    cursor.execute('insert into files(dt, filetype, filename, url, status, message) values(?, ?, ?, ?, ?, ?)', now, filetype, filename, url, status, message)
    connection.commit()

def log_files_forecast(filetype, filename, url, status, message,starttime,filecount=0,elapsedtime=0,year='0000',month='00',day='00',forecast='0000',windpark=''):
    message = message[0:4000]
    now = datetime.now(tz=timezone.utc)
    connection_string = get_connection_string()
    connection = get_connection(connection_string=connection_string)
    cursor = connection.cursor()
    cursor.execute('insert into files(dt, filetype, filename, url, status, message, forecast,filecount,elapsedtime,year,month,day,starttime,windpark) values(?, ?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?)', now, filetype, filename, url, status, message, forecast,filecount,elapsedtime,year,month,day,starttime,windpark)
    connection.commit()

def log(severity, message):
    now = datetime.now(tz=timezone.utc)
    connection_string = get_connection_string()
    connection = get_connection(connection_string=connection_string)
    cursor = connection.cursor()
    cursor.execute('insert into logs(dt, severity, message) values(?, ?, ?)', now, severity, message)
    connection.commit()

def log_application(severity, message, application):
    message = message[0:4000]
    now = datetime.now(tz=timezone.utc)
    connection_string = get_connection_string()
    connection = get_connection(connection_string=connection_string)
    cursor = connection.cursor()
    cursor.execute('insert into logs(dt, severity, message, application) values(?, ?, ?, ?)', now, severity, message, application)
    connection.commit()

def log_application_park(severity, message, application, windpark):
    message = message[0:4000]
    now = datetime.now(tz=timezone.utc)
    connection_string = get_connection_string()
    connection = get_connection(connection_string=connection_string)
    cursor = connection.cursor()
    cursor.execute('insert into logs(dt, severity, message, application, park) values(?, ?, ?, ?, ?)', now, severity, message, application, windpark)
    connection.commit()