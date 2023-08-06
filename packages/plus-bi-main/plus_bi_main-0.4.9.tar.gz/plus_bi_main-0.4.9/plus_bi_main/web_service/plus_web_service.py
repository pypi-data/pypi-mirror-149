import logging  
import requests

class PlusWebService():
    def __init__(self,api_url):
        self.api_url = api_url

    def call_api(self, parameters):
        response = requests.get(self.api_url, params=parameters)
        res_dict = response.json()
        msg = res_dict['message']
        if response.status_code >= 500:
            logging.error('[!] [{0}] Server Error'.format(response.status_code))
            return None
        elif response.status_code == 404:
            logging.error('[!] [{0}] URL not found: [{1}]'.format(response.status_code,self.api_url))
            return None
        elif response.status_code == 401:
            logging.error('[!] [{0}] Authentication Failed'.format(response.status_code))
            return None
        elif response.status_code == 400:
            logging.error('[!] [{0}] Bad Request'.format(response.status_code))
            return None
        elif response.status_code >= 300 and response.status_code < 400:
            logging.error('[!] [{0}] Unexpected Redirect'.format(response.status_code))
            return None
        elif response.status_code == 200:
            return response.json()
        else:
            logging.error('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, msg))

        return None   
    