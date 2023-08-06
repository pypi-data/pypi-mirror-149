import logging  
import os
from typing import Type
import json
import pandas as pd
import uuid
from pandas.core.frame import DataFrame
import pyodbc
from batch import plus_batch
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
    
class PlusSubbatch():
    def __init__(self):        
        self.destination_filetype=None
        self.number_of_records=0
        self.number_of_records_in_table = 0
        self.database=None
        self.database_schema=''
        self.database_table=''
        self.create_datetime=plus_helper.getcurrent_datetime()
        self.end_datetime=None
        self.message_version=''
        self.web_service=None
        self.api_url=None
        self.report=None
        self.inserted_into_batch_files=True
        self.cds_batchid = None
        self.destination_account=''
        self.destination_container=''
        self.destination_folder=''
        self.cds_batchaction=''
        self.primary_key_fields=[]

    def init_onramp(self, batch):
        if not isinstance(batch, plus_batch.PlusBatch):
            logging.info(f'Passed {type(batch)}, expecting object of Batch-type')
        self.cds_batchid=batch.cds_batchid
        self.source_filename=batch.source_filename
        self.source_folder=batch.source_folder
        self.business_object_type=batch.business_object_type

        self.batch=batch

        self.state = 'Init' 
        self.inserted_into_batch_files=False      

        self.set_subbatchid()

    def set_database_connection(self, server, database_name, username, password):
        if isinstance(server, str) and isinstance(database_name, str) and isinstance(username, str) and isinstance(password, str):
            #Auto retry logic for when database is down is applied in Database module
            self.database=plus_database.PlusDatabase(server=server, name=database_name, username=username, password=password)
        else:
            self.database=None
            raise TypeError(f'One of the passed variables is not of type str.')

    def set_subbatchid(self, subbatch=''):
        if subbatch=='':
            self.cds_subbatchid = str(uuid.uuid4())
        else:
            self.cds_subbatchid = subbatch

    def set_target_filetype(self, dest_filetype='json'):
        if isinstance(dest_filetype, str):
            self.destination_filetype=dest_filetype
        else:
            raise TypeError(f'Expected str-input for dest_filetype variable.')
    
    def set_web_service(self, api_url=None):
        if not api_url:
            raise ValueError('Expected a valid URL for Web Service API.')        
        self.api_url = api_url
        self.web_service = plus_web_service.PlusWebService(api_url=self.api_url)

    def get_filename(self, split_attributes='', split_values=''):
        if split_attributes == '' or split_values == '':
            split_zip = ''
        elif isinstance(split_attributes, (str, tuple, list)) and isinstance(split_values, (str, tuple, list)):
            split_attr_new = [item.lower() for item in split_attributes]
            split_zip = zip(split_attr_new, split_values)
        else:
            logging.info('Expected empty values or values of type string, tuple or list for "split_attributes" and "split_values" variables.')
            return False
        
        split_zip_new=''
        for item in split_zip:
            split_zip_new+="_" + "_".join(item)

        #we expect the source filename to be formatted like this:
        # YYYY_{period_letter(P(eriode),W(eek),M(aand))}{PeriodeNumber(XX)}_{BusinessObject}.{filetype}
        #ie. 2021_W20_dvo-omzet.xlsx
        if not self.destination_filetype:
            self.set_target_filetype()

        self.year = self.source_filename.split('_')[0]
        self.period = self.source_filename.split('_')[1]
        self.destination_folder=f'{self.year}/{self.period}'
        self.destination_filename = f'{self.destination_folder}/{self.year}_{self.period}{split_zip_new}_{self.business_object_type}_{self.cds_subbatchid}.{self.destination_filetype}'

        return self.destination_filename

    def set_report_message(self, action, call_type='result'):
        if call_type == 'result':
            self.report = {
                        "SubBatch": { 
                        "CDS_SubBatchId": self.cds_subbatchid,
                        "CDS_BatchId": self.cds_batchid,                      
                        "BatchCreateDate": self.create_datetime,
                        "BatchEndDate": self.end_datetime,
                        "Accountname": self.destination_account,
                        "Containername": self.destination_container,
                        "Foldername": self.destination_folder,
                        "Filename": self.destination_filename, #has to be without path
                        "NumberOfRecords": self.number_of_records,
                        "NumberOfRecordsInTable": self.number_of_records_in_table,
                        "State": self.state,                      
                        "Action": action,
                        "ErrorId": ''
                        }
                    }
        elif call_type=='retrieve':
                self.report = {
                        "SubBatch": { 
                        "CDS_SubBatchId": self.cds_subbatchid,
                        "Filename": '',
                        "State": self.state,       
                        "Action": action
                        }
                    }
        else:
            logging.error('Unknown type of report')
        return self.report

    def send_batchfiles_report(self, destination_type, action):
        if destination_type == 'web_service':
            if not self.report or self.report['SubBatch']["Action"]!=action :
                self.report = self.set_report_message(action=action) 
        
            if not self.web_service:
                logging.error('SubBatch: Web service not set...')
                raise ConnectionError('Unable to send report to web_service, aborting. See previous messages...')

            if self.report['SubBatch']['Action'] =='insert' and self.inserted_into_batch_files:
                self.report = self.set_report_message(action='update')

            subbatch_report = self.report['SubBatch']
            parameters = { "key": f"{subbatch_report['Action']}", "value": f"{json.dumps(subbatch_report)}" }

            res = self.web_service.call_api(parameters=parameters)

            if res['message'] != 'Success':
                logging.error(f'API call unsuccessful: {res}')
                raise RuntimeError('Error occured, see previous messages...')

            self.inserted_into_batch_files=True

        elif destination_type == 'direct_sql':
            if not self.database and self.batch.database:
                self.database = self.batch.database
            else:
                raise pyodbc.DatabaseError('No database connection found. Aborting...')

            if action == 'insert':
                sql = f"""INSERT INTO [IL_CTRL].[CDS_BatchFiles]
                        ([CDS_BatchId]
                        ,[CDS_SubBatchId]
                        ,[BatchCreateDate]
                        ,[BatchEndDate]
                        ,[Accountname]
                        ,[Containername]
                        ,[Foldername]
                        ,[Filename]
                        ,[NumberOfRecords]
                        ,[NumberOfRecordsInTable]
                        ,[State]
                        ,[ErrorId])
                        VALUES
                        (
                        '{self.batch.cds_batchid}'
                        ,'{self.cds_subbatchid}'
                        ,'{self.create_datetime}'
                        ,NULL
                        ,'{self.destination_account}'
                        ,'{self.destination_container}'
                        ,'{self.destination_folder}'
                        ,'{self.destination_filename}'
                        ,{self.number_of_records}                        
                        ,0
                        ,'{self.state}'
                        ,NULL
                        )"""
                self.database.execute_insert_query(sql)
            elif action == 'update':
                
                sql = f"""UPDATE [IL_CTRL].[CDS_BatchFiles]
SET [NumberOfRecords] = {self.number_of_records}
,[State] = '{self.state}'
,[NumberOfRecordsInTable] = {self.number_of_records_in_table}
,[BatchEndDate] = {f'{self.database.null_value}' if self.state not in ('Done', 'Error', 'Processed') else f"'{plus_helper.getcurrent_datetime()}'"}
WHERE SubBatchId = '{self.cds_subbatchid}'"""
                self.database.execute_insert_query(sql)
                
    def _get_onramp_msg_header(self):
        onramp_msg_header = {
                "messageType": self.batch.business_object_type,
                "creationDateTime": self.create_datetime,
                "Filename" : self.destination_filename,
                "Foldername" : self.destination_folder,
                "numberOfRecords" : self.number_of_records,
                "CDS_BatchId" : self.batch.cds_batchid, 
                "CDS_SubBatchId" : self.cds_subbatchid,
                "CDS_BatchAction": self.cds_batchaction,
                "RapportageJaar" : self.year,
                "Rapportageperiode" : self.period[1:],
                "MessageVersion": self.message_version,
                "PrimaryKeyFields": self.primary_key_fields,
                "payload": []
            }
        return onramp_msg_header

    def _create_msg(self, df):
        self.msg = self._get_onramp_msg_header()

        records = json.loads(DataFrame(df).to_json(orient='records', date_format='iso'))
   
        for r in records:
            r['CDS_BatchId'] = self.batch.cds_batchid 
            r['CDS_SubBatchId'] = self.cds_subbatchid
            r['RapportageJaar'] = self.year
            r['Rapportageperiode'] = self.period[1:]
            record = {"record": r}
            
            payload = self.msg['payload']
            payload.append(record)
    
    def get_msg_with_data(self, df):
        if not isinstance(df, DataFrame):
            raise TypeError(f"Provided data in variable df is not a DataFrame. Can't process data.")
        
        self.number_of_records=df.shape[0]
        self._create_msg(df=df)

        return self.msg
        
    def get_cds_notification_msg(self, action):
        self.notification_msg={
            "notification": {
                "MessageType": "cds-notificatie",
                "CDS_BatchId": self.cds_batchid,
                "CDS_SubBatchId": self.cds_subbatchid,
                "CreationDateTime": plus_helper.gettime_epoch(),
                "Accountname": self.destination_account,
                "Containername": self.destination_container,
                "Foldername": self.destination_folder,
                "Filename": self.destination_filename,
                "NumberOfRecords": self.number_of_records,
                "EtlRunStatus": self.state,
                "MessageVersion": self.message_version,
                "Action": action}
        }
        return json.dumps(self.notification_msg)

    def file_was_processed(self, blob):
        #a blob is expected to be a combination of folder and filename joined by a "/" ie. "2021/20/2021_P20_oos.xlsx"
        #the folder is optional.
        sql = f"SELECT COUNT(filename) as qty FROM BatchFiles WHERE filename = '{blob}' AND State IN ('Done')"
        result = self.database.execute_select_query(sql)

        if result:
            if result[0].qty > 0:
                return True
            else:
                return False
        else:
            logging.info('Something went wrong when checking if the file was processed, see previous error messages.')
    
    def get_batchfiles_info(self):
        if self.cds_subbatchid=='':
            raise ValueError('Cds_subbatchid not set, exiting process...')

        if not self.web_service:
            logging.info('Trying to get BatchFiles info through Database connection...')
            if not self.database:
                raise ValueError('Database connection not set, use Class Method "set_database_connection()"...')
            else:
                sql = f"""SELECT [Id]
        ,[CDS_BatchId]
        ,[CDS_SubBatchId]
        ,[BatchCreateDate]
        ,[BatchEndDate]
        ,[Accountname]
        ,[Containername]
        ,[Foldername]
        ,[Filename]
        ,[NumberOfRecords]
        ,[NumberOfRecordsInTable]
        ,[State]
        ,[ErrorId]
    FROM [IL_CTRL].[CDS_BatchFiles]
    WHERE CDS_SubBatchId = '{self.cds_subbatchid}' 
    AND state = '{self.state}'"""
                result = self.database.execute_select_query(sql)                
        else:
            logging.info('Trying to get BatchFiles info through Web Service connection...')
            if not self.report:
                self.report = self.set_report_message(action='select', call_type='retrieve')
            else:
                self.report['Action'] = 'select'
            subbatch_report = json.dumps(self.report['SubBatch'])
            
            parameters={ "key": f"select", "value": f"{subbatch_report}" }
            result = self.web_service.call_api(parameters=parameters)

        if not result:
            logging.info(f"Couldn't retrieve SubBatch/BatchFiles information, can't continue...")
            raise AssertionError(f'No records with state "ReadyForPickup" found for CDS_SubbatchID: {self.cds_subbatchid}.\nAborting.')
        else:
            if not self.web_service:
                logging.info('Setting variables from SQL Query result in the subbatch...')
                self.cds_batchid=result[0].CDS_BatchId
                self.number_of_records = result[0].NumberOfRecords
                self.destination_account = result[0].Accountname
                self.destination_container = result[0].Containername
                self.destination_folder = result[0].Foldername
                self.destination_filename = result[0].Filename
            else:
                logging.info('Setting variables from API-call result in the subbatch...')
                info = json.loads(result["Info"])["BatchFilesInfo"][0]

                self.cds_batchid=info["CDS_BatchId"]
                self.number_of_records=info["NumberOfRecords"]
                self.destination_account=info["AccountName"]
                self.destination_container=info["ContainerName"]
                self.destination_folder=info["FolderName"]
                self.destination_filename=info["FileName"]
            