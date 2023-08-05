import logging  
import os
from azure.storage.blob import generate_blob_sas, BlobServiceClient, BlobClient, ContainerClient, AccountSasPermissions
from datetime import datetime, timedelta
import json

class PlusStorage():
    def __init__(self, storage_cnxn_string):
        #incoming: 'DefaultEndpointsProtocol=https;AccountName=plsdevcdsdata;AccountKey=JsvdRXFZvhprZx/34/dwiP0gsN44hUyvz9mhK0yHelu7cMFRpwtvyyxepXY9wW97O5CzLgnD4yXiIjCsM61I/Q==;EndpointSuffix=core.windows.net'
        string_array = storage_cnxn_string.split(';')
        if len(string_array) == 1:
            logging.info(f'Invalid connection string provided for storage account:\n{storage_cnxn_string}')
        else:
            self.default_endpoints_protocol=string_array[0].replace('DefaultEndpointsProtocol=','')
            self.account_name=string_array[1].replace('AccountName=','')
            self.account_key=string_array[2].replace('AccountKey=','')
            self.endpoint_suffix=string_array[3].replace('EndpointSuffix=','')
            try:
                self.blob_service_client=BlobServiceClient.from_connection_string(storage_cnxn_string)
            except Exception as e:
                logging.info(f"Can't establish connection through provided connection string:\n{storage_cnxn_string}")
        
    def get_url_for_blob(self, container='', folder='', filename=''):
        if isinstance(container, str) and isinstance(folder, str) and isinstance(filename, str):       
            if container == '' or filename == '':
                logging.info(f'Need to provide at least a container and filename.')
                return None
            if folder != '':
                if folder.endswith('/'):
                    blob_name = folder + filename
                else:
                    blob_name = folder + '/' + filename
            else:
                blob_name = filename
        try:
            sas_token_blob = generate_blob_sas(
                                                account_name=self.account_name,
                                                account_key=self.account_key,
                                                container_name= container,
                                                blob_name = blob_name,
                                                snapshot=None,
                                                permission=AccountSasPermissions(read=True),
                                                expiry=datetime.utcnow() + timedelta(hours=1)
                                                )
            url = 'https://' + self.account_name + '.blob.core.windows.net/' + container + '/' + blob_name + '?' + sas_token_blob
            return url
        except Exception as ex:
            logging.error('Error 0: %s', ex.args[0])
            logging.error('Error 1: %s', ex.args[1])
            return None
    
    def upload_file(self, data, container, blob): 
        #blob is expected to be of form: {optional: folder}/{mandatory:filename with subbatchid} ie. 2021/06/2021_P06_oos_{subbatchid}.json               
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container, blob=blob)
            blob_client.upload_blob(data, overwrite=True)
        except Exception as e:
            logging.error('Trying to upload error %s', e)
            logging.error(e.args[0])

    def get_data_as_text(self, datastream, encoding='Utf-8'):
        #blob is the combination of folder and filename
        #this will return the data inside the blob as text (mainly used when loading csv)
        return datastream.content_as_text(encoding=encoding)

    def get_data_as_bytes(self, datastream):
        #blob is the combination of folder and filename
        #this will return the data inside the blob as bytes
        return datastream.content_as_bytes()

    def download_file(self, container, blob):
        try:
            blob_client =BlobClient.from_blob_url(self.get_url_for_blob(container=container, folder="/".join(blob.split("/")[0:-1]), filename=blob.split("/")[-1]))
            return blob_client.download_blob()
        except Exception as ex:
            logging.error(f'Error: {ex}\nFailed to download Blob: {blob}\nContainer: {container}\nAccount: {self.account_name}')






