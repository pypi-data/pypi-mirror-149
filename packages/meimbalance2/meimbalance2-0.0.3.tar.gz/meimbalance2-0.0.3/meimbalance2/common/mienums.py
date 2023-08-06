from enum import Enum

class OsPlatform(str, Enum):
    windows = 'Windows'
    linux = 'Linux'
    java = 'Java'

class SqlProtocol(str, Enum):
    password = 'SqlPassword'
    integrated = 'ActiveDirectoryIntegrated'
    interactive = 'ActiveDirectoryInteractive'
    msi = 'ActiveDirectoryMsi'

class Datalakes(str, Enum):
    imbalance_dev =  'aezstoimbalancedevstore'
    imbalance_prd =  'aezstoimbalanceprdstore'