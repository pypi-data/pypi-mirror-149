import logging  
import uuid
import pyodbc
import json
import requests
from helper import plus_helper
from database import plus_database
from web_service import plus_web_service

#incoming Event (filename/url)

#class Batch (input= source_filename/url, 
#                  store: batchid, start_datetime, end_datetime, Source_filename, businessobjecttype, filetype, source_path, number_of_records, number_of_files, state
#                   generate: BatchId)
    #Generate BatchId
    #check if filename is correct and file exists
    #check if file was already handled
    #report (send message to queue BatchSummary)

#class SubBatch (input = batchid,
#                   store: subbatchid, start_datetime, end_datetime, target_filename, target_folder, 
#                           target_container, number_of_records, state
#                   generate: subbatchid, destination filename (input is filter in file and objecttype) and path,  )
    #Generate Subbatchid
    #Generate target filename and path
    #Report (Query now, API later)
    
class PlusBatch():
    def __init__(self, cds_batchid=''):
        self.cds_batchid = cds_batchid 
        self.number_of_records = 0         
        self.state = ''
        self.api_url = None
        self.web_service=None
        self.inserted_into_batch_summary=None
        self.batch_start_datetime = plus_helper.getcurrent_datetime()
        self.report=None

    def init_onramp(self, file_url, business_object_type):
        if not self._is_valid_url(file_url):
            raise ValueError(f'Provided uri is invalid: {file_url}')
        if not self._has_valid_ext():
            raise AssertionError(f'Provided filetype is not supported: {self.filetype}')
        self.cds_batchid = str(uuid.uuid4())
        self.number_of_files = 0
        self.state = 'Init'
        self.business_object_type=str(business_object_type).lower()
        self.inserted_into_batch_summary=False

        self.service_name=f'plus-bi-{business_object_type}-onramp-storageblob'
        self.message_type=f'plus-bi-{business_object_type}'

        self._set_storage_info()

    def _is_valid_url(self, file_url):
        if 'https://' in file_url.lower():
            self.url=file_url
            return True
        else:
            return False

    def _has_valid_ext(self):
        extensions = ('xlsx','xls','json','csv','parquet','xml')
        self.filetype = self.url.split('.')[-1]
        if self.filetype in extensions:
            return True
        else:
            return False
    
    def _has_correct_filename(self):
        # check if filename contains a year, a period and the expected businesstype
        #how to handle IIB: 2021_05_18_cds_pos01_cds_digitalreceipt_08ac77bd-fff7-4a8a-b20a-67600250c549.json

        logging.info(f'Checking if filename ({self.source_filename}) is valid.')
                
        filenamearray = self.source_filename.split('_')
        file_extension_array = self.source_filename.split('.')

        if isinstance(file_extension_array, (list, tuple)):
            self.file_extension=str(file_extension_array[-1]).lower()
        elif isinstance(file_extension_array, str):
            logging.info(f'It looks like there is no file extension present: {self.source_filename}')
            return False
        else:
            logging.info(f'Unexpected type for file_extension_array: {type(file_extension_array)}')
            return False

        if len(filenamearray) < 3:
            logging.info('Shape of incoming filename is unexpected, filename is NOT valid.')
            return False
        elif ((len(filenamearray[0]) == 4 and len(filenamearray[1]) == 2 and len(filenamearray[2]) == 2 and filenamearray[-1].endswith("json")) or 
              (len(filenamearray[0]) == 4 and len(filenamearray[1]) == 2 and len(filenamearray[2]) == 2 and filenamearray[-1].endswith("csv"))) :
            #this looks like an IIB message, we don't grab information for the onramp for these messages and so we need to set them ourself.
            logging.info('Looks like an IIB filename.')
            self.year = filenamearray[0]
            #we can't grab the period from the filename in IIB-flows, we set it to Period 99 which is non-existent in practice.
            self.period = 'P99'
            #there is a test later on where we determine if the correct businessobject was passed, in non-IIB flows we grab the 
            #businessobject from the filename to check if they match, here we set the value to itself.
            businesstype = self.business_object_type
        else:
            self.year = filenamearray[0]
            self.period = filenamearray[1]
            businesstype = str(filenamearray[2]).lower()

        try: 
            year = int(filenamearray[0])
            if year < 2099 and year >= 2000:
                logging.info('Valid year provided in filename.')
        except Exception as e:
            logging.error(f'{e}: {year} is not a valid year in {self.source_filename}')        
        
        try: 
            if not self.period.startswith(('P','W','M')):
                raise AssertionError(f'Unexpected value where period is expected in filename. Value: {self.period}, should start with "P"(Period),"W"(week) or"M"(Month).')
        except Exception as e:
            logging.error(f'{e}: {self.period} is not a valid period in {self.source_filename}')        
        
        if self.business_object_type == '':
            raise AssertionError(f'Business Object Type not set, first use method "set_business_object_type(self, business_object_type)" in this Class.')
        if not businesstype.lower().startswith(self.business_object_type):
            logging.error(f'{businesstype} is not of the expected value: {self.business_object_type}')
            return False

        return True

    def _set_storage_info(self):
        self.source_filename=self.url.split('/')[-1]

        if not self._has_correct_filename():
            raise AssertionError(f'Filename is not as expected. See previous messages...')

        self.source_url_account=plus_helper.split_custom_char(self.url, '/', 3)
        self.source_account=self.source_url_account.split('.')[0].split('/')[-1]
        self.source_container_and_folder=self.url.replace(self.source_url_account, '').replace(self.source_filename, '')
        self.source_container=self.source_container_and_folder.split('/')[1]
        self.source_folder='/'.join(self.source_container_and_folder.split('/')[2:])[:-1]

        self.destination_folder=self.year + '/' + self.period

    def _set_onramp_filename(self, dest_filename):
        #during processing we split the sourcefile based on one or more attributes.
        #On subbatch level we determine the filename
        pass

    def set_database_connection(self, server, database_name, username, password):
        if isinstance(server, str) and isinstance(database_name, str) and isinstance(username, str) and isinstance(password, str):
            #Auto retry logic for when database is down is applied in Database module
            self.database=plus_database.PlusDatabase(server=server, name=database_name, username=username, password=password)
        else:
            self.database=None
            raise TypeError(f'One of the passed variables is not of type str.')
    def set_web_service(self, api_url=None):
        if not api_url and not self.api_url:
            raise ValueError('Expected a valid URL for Web Service API.')
        elif api_url and not self.api_url:
            self.api_url = api_url
        
        self.web_service = plus_web_service.PlusWebService(api_url=self.api_url)

    def file_was_processed(self):
        logging.info(f'Check if file {self.source_filename} was already processed.')
        if not self.web_service and self.api_url:
            self.set_web_service(api_url=self.api_url)
            logging.info(f'Web Service variable is of type: {type(self.web_service)}')
        if not self.report:
            self.set_report_message(action='insert')

        if self.web_service:            
            batch_report = json.dumps(self.report['Batch'])
            
            parameters={ "key": "check_if_processed", "value": f"{batch_report}" }
            res = self.web_service.call_api(parameters=parameters)

            if not res or res['message'] != 'File not yet processed.':
                logging.error('File was already processed.')
                return True
            else:
                return False
        else:
            sql = f"SELECT COUNT(filename) as qty FROM IL_CTRL.CDS_BatchSummary WHERE filename like '%{self.source_filename}'"
        
            result = self.database.execute_select_query(sql)

            if result:
                if result[0].qty > 0:
                    return True
                else:
                    return False
            else:
                logging.info('Something went wrong when checking if the file was processed, see previous error messages.')


    def set_report_message(self, action):
        self.report = {
                    "Batch": { 
                      "CDS_BatchId": self.cds_batchid,                      
                      "BatchCreateDate": self.batch_start_datetime ,
                      "Accountname": self.source_account,
                      "Containername": self.source_container,
                      "Foldername": self.source_folder,
                      "Filename": self.source_filename, #has to be without path
                      "NumberOfRecords": self.number_of_records,
                      "NumberOfFiles": self.number_of_files,
                      "State": self.state,                      
                      "Action": action,
                      "ErrorId": ''
                      }
                  }
        return self.report

    def send_report(self, destination_type, api_url=''):
        #destination_type valid entries: web_service, direct_sql
        if not self.report:
            self.set_report_message(action='insert')        
        
        if self.report['Batch']['Action'] == 'insert' and self.inserted_into_batch_summary:
            self.set_report_message(action='update')

        batch_report = self.report['Batch']
        if destination_type == 'web_service':
            if not self.web_service:
                logging.error('Batch: Web service not set...')
                raise ConnectionError('Unable to send report to web_service, aborting. See previous messages...')

            parameters = { "key": f"{batch_report['Action']}", "value": f"{json.dumps(batch_report)}" }

            res = self.web_service.call_api(parameters=parameters)

            if res['message'] != 'Success':
                logging.error('API call unsuccessful: {res}')
                raise RuntimeError('Error occured, see previous messages...')
            self.inserted_into_batch_summary = True
            
        elif destination_type == 'direct_sql':
            if batch_report['Action'].lower() == 'insert':
                sql = f"""INSERT INTO [IL_CTRL].[CDS_BatchSummary]
                        ([CDS_BatchId]
                        ,[BatchCreateDate]
                        ,[Filename]
                        ,[NumberOfRecords]
                        ,[NumberOfFiles]
                        ,[State]
                        ,[Accountname]
                        ,[Containername]
                        ,[Foldername])
                        VALUES
                        ('{self.cds_batchid}'
                        ,'{batch_report['BatchCreateDate']}'
                        ,'{batch_report['Filename']}'
                        ,{batch_report['NumberOfRecords']}
                        ,{batch_report['NumberOfFiles']}
                        ,'{batch_report['State']}'
                        ,'{batch_report['Accountname']}'
                        ,'{batch_report['Containername']}'
                        ,'{batch_report['Foldername']}')"""
                self.database.execute_insert_query(sql)                
            elif batch_report['Action'].lower() == 'update':
                sql = f"""UPDATE [IL_CTRL].[CDS_BatchSummary]
                        SET [NumberOfRecords] = {batch_report['NumberOfRecords']}
                        ,[NumberOfFiles] = {batch_report['NumberOfFiles']}
                        ,[State] = '{batch_report['State']}'
                        WHERE [CDS_BatchId] = '{self.cds_batchid}'"""
                self.database.execute_update_query(sql)

    def create_error_message(self, error_code, error_description):
        self.error_msg = { "CDS_BatchId": self.cds_batchid,
                            "MessageId": str(uuid.uuid4()),
                            "MessageType" : self.message_type + '_Error',
                            "ErrorDateTime" : plus_helper.getcurrent_datetime(),
                            "BatchFilename": self.source_filename,
                            "ErrorFilename":"",
                            "Errors":[{
                                "Servicename": self.service_name,
                                "ErrorCode": error_code,
                                "ErrorDescription": error_description
                            }],
                            "payload" : []
                            }
        return self.error_msg
