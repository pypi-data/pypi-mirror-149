import os
import tempfile
import logging
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
import pandas as pd

from ._Datalake import Datalake
from ..common.mienums import Datalakes
from ..common.env import (
    IMBALANCE_DATALAKE_NAME_DEV,
    IMBALANCE_DATALAKE_NAME_PRD
)

_logger = logging.getLogger(__name__)

# Class to handle Gen2 Datalakes
class DatalakeGen2(Datalake):
    def __init__(self,datalake_name, azure_credential, copy_instance=False, container_name: str = 'root', lazy_loading: bool = True):
            self._datalake_name = datalake_name
            self._azure_credential = azure_credential
            self._container_name = container_name

            # Instantiate attribute for the copy target
            self._copy_datalake = None
            # Add code to cache service client
            super().__init__(datalake_name)
            self.__service_client = self.__get_service_client()
            # Add code to cache file system client
            self.__file_system_client = self.__get_file_system_client()

            if copy_instance:
                return

            
            # Initiate a new instance of the DatalakeGen2 class to handle Dev connections
            if self.copy_to_target == True and not lazy_loading:
                self.copy_datalake

    @property
    def container_name(self) -> str:
        return self._container_name
    
    @container_name.setter
    def container_name(self, val: str) -> None:
        self._container_name = val

    
    @property
    def datalake_name(self) -> str:
        return self._datalake_name
    
    @datalake_name.setter
    def datalake_name(self, val: str) -> None:
        self._datalake_name = val
    
    @property
    def copy_to_dev(self) -> bool:
        return os.environ.get('COPY_TO_DEV', 'FALSE').upper() == 'TRUE'

    @property
    def copy_to_prod(self) -> bool:
        return os.environ.get('COPY_TO_PROD', 'FALSE').upper() == 'TRUE'
    
    @property
    def running_in_prod(self) -> bool:
        return self.datalake_name == str(Datalakes.imbalance_prd)

    @property
    def running_in_dev(self) -> bool:
        return self.datalake_name == str(Datalakes.imbalance_dev)

    @property
    def copy_to_target(self) -> bool:
        if self.running_in_prod:
            return self.copy_to_dev
        elif self.running_in_dev:
            return self.copy_to_prod
        return False
    
    @property
    def copy_target(self) -> str:
        if self.running_in_prod:
            target_name = os.environ.get(IMBALANCE_DATALAKE_NAME_DEV, None)
            if target_name is None:
                raise EnvironmentError(f"{IMBALANCE_DATALAKE_NAME_DEV} has to be defined when copying to dev")

        else:
            target_name = os.environ.get(IMBALANCE_DATALAKE_NAME_PRD, None)
            if target_name is None:
                raise EnvironmentError(f"{IMBALANCE_DATALAKE_NAME_PRD} has to be defined when copying to production")
        
        return target_name
    
    @property
    def copy_datalake(self):
        if self.copy_to_target and self._copy_datalake is None:
            self.set_copy_instance()
        
        return self._copy_datalake


    def set_copy_instance(self):
        if self.copy_to_target:
            self._copy_datalake = DatalakeGen2(self.copy_target, self._azure_credential, copy_instance=True)
    
    

    # Get a service client
    def __get_service_client(self):
        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", self.datalake_name), credential=self.azure_credential)
        return service_client

    # Get a file system client for the given root
    def __get_file_system_client(self):
        # service_client = self.__get_service_client()
        file_system_client = self.__service_client.get_file_system_client(file_system=self.container_name)
        return file_system_client

    # Get a directory client for the given directory_name
    def __get_directory_client(self, directory_name):
        file_system_client = self.__file_system_client
        try:
            directory_client = file_system_client.get_directory_client(directory=directory_name)
        except Exception as e:
            print('Error in getting directory client for ', directory_name, ': ', e)
            return None

        return directory_client

    # Get a file client for the given directory and file name
    def __get_file_client(self, directory_name, filename):
        directory_client = self.__get_directory_client(directory_name)
        file_client = directory_client.get_file_client(filename)
        return file_client

    # Helper function to download a file
    def __download_file(self, directory_name, filename, file):
        file_client = self.__get_file_client(directory_name, filename)
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        file.write(downloaded_bytes)
        file.seek(0,0)
        return

    # Helper function to check if a file exists
    def __check_if_file_exists(self, directory_name, filename):
        if directory_name == '/':
            file_path = filename
        else:
            file_path = directory_name[1:] + '/' + filename
        file_system_client = self.__file_system_client
        try:
            paths = file_system_client.get_paths(path=directory_name, recursive=False)
            for path in paths:
                if file_path == path.name:
                    return True

        except:
            # If we cant find the path, then just return False
            return False 

        return False

    # List content of a directory
    def list_files_in_directory(self, directory_name):
        file_system_client = self.__file_system_client
        files = []
        paths = file_system_client.get_paths(path=directory_name, recursive=False)
        for path in paths:
            directory_name, filename = os.path.split(path.name)
            files.append(filename)
        return files

    # Get newest file in directory
    def get_latest_file_in_directory(self, directory_name):
        files_df = self.list_files_attributes_in_directory(directory_name=directory_name)
        count = len(files_df)
        if count == 0:
            return None

        files_df.sort_values(by=['last_modified','filename'],ascending=False, inplace=True)
        file_df = files_df[['filename']].head(1)
        filename = file_df.iloc[0]['filename']
        return filename

    # Get Dataframe with directory listing
    def list_files_attributes_in_directory(self, directory_name):
        file_system_client = self.__file_system_client
        names = []
        etags = []
        deleteds = []
        metadatas = []
        last_modifieds = []
        creation_times = []
        sizes = []

        paths = file_system_client.get_paths(path=directory_name, recursive=False)
        count = 0
        for path in paths:
            directory_name, filename = os.path.split(path.name)
            file_client = self.__get_file_client(directory_name, filename)
            properties = file_client.get_file_properties()
            if  not(('hdi_isfolder') in properties.metadata and properties.metadata['hdi_isfolder'] == 'true'):
                count = count + 1
                names.append(filename)
                etags.append(properties.etag)
                deleteds.append(properties.deleted)
                metadatas.append(properties.metadata)
                last_modifieds.append(properties.last_modified)
                creation_times.append(properties.creation_time)
                sizes.append(properties.size)

        data = {'filename':names, 'etag': etags, 'deleted': deleteds, 'metadata': metadatas, 'last_modified': last_modifieds, 'creation_time': creation_times, 'size': sizes}
        dataframe = pd.DataFrame(data=data)
        return dataframe


    # Download a file from the datalake, write it to a local temporary file, and open the file for processing
    def open_file(self, directory_name, filename): 
        localfile=tempfile.TemporaryFile()
        self.__download_file(directory_name, filename, localfile)
        localfile.seek(0,0)
        return localfile

    # Download a file from the datalake, write it to a local temporary file, and open the file for processing
    def open_text_file(self, directory_name, filename): 
        file_client = self.__get_file_client(directory_name, filename)
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        downloaded_text = downloaded_bytes.decode("utf-8")
        localfile=tempfile.TemporaryFile(mode='a+t')
        localfile.writelines(downloaded_text)
        localfile.seek(0,0)
        return localfile

    # Upload a local file to a new file in the Datalake
    def upload_file(self, file, directory_name, filename, overwrite=False):
        file.seek(0,0)
        file_contents = file.read()
        directory_client = self.__get_directory_client(directory_name)
        
        # Check if file already exist in the lake if Owerwrite is False
        if overwrite == False:
            if self.__check_if_file_exists(directory_name=directory_name, filename=filename):
                _logger.error('File ' + filename + ' already exists in directory ' + directory_name)
                return

        directory_client.create_file(file=filename)
        file_client = directory_client.get_file_client(filename)
        file_client.append_data(data=file_contents, offset=0, length=len(file_contents))
        file_client.flush_data(len(file_contents))

        # If copy-to-dev is set, then upload to dev also
        if self.copy_to_target == True:
            self.copy_datalake.upload_file(file, directory_name, filename, overwrite=True)

    # Upload a local named file to the datalake
    def upload_local_file(self, local_filepath, directory_name, filename, overwrite=False):
        file=open(local_filepath,"rb")
        self.upload_file(file, directory_name, filename, overwrite=overwrite)
        file.close()

        # Download a file to a local filesystem
    def download_to_local_file(self, directory_name, filename, local_filepath):
        file=open(local_filepath, "wb")
        self.__download_file(directory_name, filename, file)
        file.close()
        pass