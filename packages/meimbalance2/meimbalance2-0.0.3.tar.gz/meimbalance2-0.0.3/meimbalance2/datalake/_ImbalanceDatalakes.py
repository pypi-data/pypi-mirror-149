import logging
import os

from azure.identity import DefaultAzureCredential
from ._DatalakeGen2 import DatalakeGen2

from ..common.env import (
    IMBALANCE_DATALAKE_NAME,
    SHARED_DATALAKE_NAME,
    SHARED_DATALAKE_NAME_GEN2
)

# Helper class to initialize instances for the 3 datalakes in use in the project and 
# get Azure Credentials and token
class ImbalanceDatalakes:
    def __init__(self, exclude_managed_identity_credential: bool = False, stdout_logging: bool = False, lazy_loading: bool = True):
        """Helper class to initialize instances for the 3 datalakes in use in the project and 
        get Azure Credentials and token.

        :param bool exclude_managed_identity_credential: Whether to exclude managed identity for data lake access, Defaults to True for backwards compatibility purposes.
        """
        self._exclude_managed_identity_credential=exclude_managed_identity_credential
        self._stdout_logging = stdout_logging
        self._lazy_loading = lazy_loading
            
        self._azure_credential = None
        self._imbalance_datalake = None
        self._shared_datalake = None

        # Force enablement of datalakes if lazy loading is disabled
        if not lazy_loading:
            self.imbalance_datalake
            self.shared_datalake

    @property
    def imbalance_datalake_name(self) -> str:
        datalake_name = os.environ.get(IMBALANCE_DATALAKE_NAME, None)

        if datalake_name is None:

            # Construct the error message
            message_components = [
                f'ERROR: Missing environment variables, need to declare {IMBALANCE_DATALAKE_NAME}',
                'Hint: Put these variables in the .env file in the project root, and create a source statement in ~/.bashrc:',
                'if [ -f ~/source/Imbalance/.env ]; then',
                '    source ~/source/Imbalance/.env',
                'fi',
                'Otherwise define them from the host.'
            ]
            message = os.linesep.join(message_components)
            
            # For backwards compatibility in stdout dependent processes
            if self._stdout_logging:
                print(message)

            # Raise error for incomplete environment
            raise EnvironmentError(message)

    @property
    def shared_datalake_name(self)  -> str:
        datalake_name = os.environ.get(SHARED_DATALAKE_NAME, os.environ.get(SHARED_DATALAKE_NAME_GEN2, None))

        if datalake_name is None:

            # Construct the error message
            message_components = [
                f'ERROR: Missing environment variables, need to declare {SHARED_DATALAKE_NAME} or {SHARED_DATALAKE_NAME_GEN2}',
                'Hint: Put these variables in the .env file in the project root, and create a source statement in ~/.bashrc:',
                'if [ -f ~/source/Imbalance/.env ]; then',
                '    source ~/source/Imbalance/.env',
                'fi',
                'Otherwise define them from the host.'
            ]
            message = os.linesep.join(message_components)
            
            # For backwards compatibility in stdout dependent processes
            if self._stdout_logging:
                print(message)

            # Raise error for incomplete environment
            raise EnvironmentError(message)

    @property
    def azure_credential(self) -> DefaultAzureCredential:
        if self._azure_credential is None:
            self._azure_credential = DefaultAzureCredential

    @property
    def imbalance_datalake(self):
        if self._imbalance_datalake is None:
            self._imbalance_datalake = DatalakeGen2(self.imbalance_datalake_name, self.azure_credential, lazy_loading=self._lazy_loading)
        
        return self._imbalance_datalake

    @property
    def shared_datalake(self):
        if self._shared_datalake is None:
            self._shared_datalake = DatalakeGen2(self.shared_datalake_name, self.azure_credential, lazy_loading=self._lazy_loading)
        
        return self._shared_datalake

    @property
    def shared_datalake_gen2(self):
        return self.shared_datalake
