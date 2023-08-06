from pathlib import Path
import os

# For storing the environment variable names used in the solution

# Saving the the ones directly mapped to their current name for future interoperability.
IMBALANCE_LOG_SERVER='IMBALANCE_LOG_SERVER'
IMBALANCE_LOG_DATABASE='IMBALANCE_LOG_DATABASE'
IMBALANCE_LOG_PROTOCOL='IMBALANCE_LOG_PROTOCOL'
IMBALANCE_LOG_USERNAME='IMBALANCE_LOG_USERNAME'
IMBALANCE_LOG_PASSWORD='IMBALANCE_LOG_PASSWORD'
IMBALANCE_LOG_ASSIGNED_UID='IMBALANCE_LOG_ASSIGNED_UID'

IMBALANCE_DATA_SERVER='IMBALANCE_DATA_SERVER'
IMBALANCE_DATA_DATABASE='IMBALANCE_DATA_DATABASE'
IMBALANCE_DATA_PROTOCOL='IMBALANCE_DATA_PROTOCOL'
IMBALANCE_DATA_USERNAME='IMBALANCE_DATA_USERNAME'
IMBALANCE_DATA_PASSWORD='IMBALANCE_DATA_PASSWORD'
IMBALANCE_DATA_ASSIGNED_UID='IMBALANCE_DATA_ASSIGNED_UID'

SENDGRID_API_KEY='SENDGRID_API_KEY'
SMS_GATEWAYAPI_TOKEN='GATEWAYAPI_TOKEN'

IMBALANCE_DATALAKE_NAME_DEV='IMBALANCE_DATALAKE_NAME_DEV'
IMBALANCE_DATALAKE_NAME_DEV='IMBALANCE_DATALAKE_NAME_PRD'

IMBALANCE_DATALAKE_NAME='IMBALANCE_DATALAKE_NAME'
SHARED_DATALAKE_NAME='SHARED_DATALAKE_NAME'
SHARED_DATALAKE_NAME_GEN2='SHARED_DATALAKE_NAME'


def check_for_multiple_env_files():
    results = _find_all(name='.env', path=str(Path.home()))
    if len(results) > 1:
        print('Warning: Multiple .env found: ' + str(len(results)))
        for result in results:
            print('  ' + result)

def _find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            if 'pythonFiles' not in root:
                result.append(os.path.join(root, name))
    return result
