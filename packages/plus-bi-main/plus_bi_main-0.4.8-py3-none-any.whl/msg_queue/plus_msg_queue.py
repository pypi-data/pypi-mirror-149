import logging  
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from helper import plus_helper

class PlusMsgQueue():
    def __init__(self,service_bus_cnxn_string):
        self.client = ServiceBusClient.from_connection_string(service_bus_cnxn_string)        

    def send_message_to_queue(self, data, queue):
        msg = ServiceBusMessage(plus_helper.encode_data(data))
        try:
                logging.debug(f'Sending report to: {queue}')                
                sender = self.client.get_queue_sender(queue)
                sender.send_messages(msg)
        except Exception as e:
                logging.error(f'Unable to process message {e}')   
    