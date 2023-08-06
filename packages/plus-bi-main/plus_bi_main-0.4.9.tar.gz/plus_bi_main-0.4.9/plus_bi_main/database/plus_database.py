import logging  
import os
import pyodbc
from helper import plus_helper

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
class PlusDatabase():
    def __init__(self, server, name, username, password):
        
        self.server = server 
        self.name = name 
        self._username = username 
        self._password = password
        self.null_value='NULL'
        self.autocommit = False

        self.cnxn = self._get_connection()
        
    @plus_helper.auto_retry(max_tries=5,wait_time_in_seconds=15)   
    def _get_connection(self):        
        try:
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.name+';UID='+self._username+';PWD='+self._password)
            return cnxn
        except pyodbc.Error as ex:
            logging.info(f'Error thrown when trying to connect to the database:')
            logging.info(f'{ex}')
            return None
    
    def execute_select_query(self, sql_command):        
        cursor = self.cnxn.cursor()
        result = None
        try:
            self.cnxn.autocommit = True
            result=cursor.execute(sql_command).fetchall()
            self.cnxn.autocommit = self.autocommit
            if result is None:
                return False
            elif isinstance(result, (pyodbc.Row, list)):               
                return result
            else:
                raise pyodbc.DatabaseError(f'Error executing query:\n"{sql_command}"')
                
        except pyodbc.DatabaseError as ex:
            logging.error(f'Error executing query, see previous errors."')
            logging.error(ex.args[0])
            logging.error(ex.args[1])
            return False

    def execute_insert_query(self, sql_command):
        cursor = self.cnxn.cursor()
        try:
            self.cnxn.autocommit = False
            cursor.execute(sql_command)
        except pyodbc.DatabaseError as ex:       
            logging.error(f'Error executing query, see previous errors."')
            logging.error(ex.args[0])
            logging.error(ex.args[1])
            cursor.rollback()
            return False
        else:
            cursor.commit()
            return True
        finally:
            self.cnxn.autocommit = self.autocommit
    
    def execute_update_query(self, sql_command):
        #code would be the same as insert
        return self.execute_insert_query(sql_command=sql_command)

    def execute_delete_query(self, sql_command):
        #code would be the same as insert
        return self.execute_insert_query(sql_command=sql_command)
        





