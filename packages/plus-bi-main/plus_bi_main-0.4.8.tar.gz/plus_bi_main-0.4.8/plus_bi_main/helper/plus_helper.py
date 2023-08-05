import logging
import time 
from datetime import datetime, timedelta
import json
import base64
import pytz

def auto_retry(max_tries=5, wait_time_in_seconds=10):
    def check(func):    
        def wrapper(*args, **kwargs):
            tries = 1
            retry = True
            while retry:      
                result_of_function = func(*args, **kwargs)
                print(f"{func.__name__}({args}, {kwargs}) Try #{tries} returned: {result_of_function}")            
                if result_of_function:
                    return result_of_function
                elif tries == max_tries:
                    return None
                else:
                    logging.info(f"{func.__name__}() returned: {result_of_function}, sleeping for {wait_time_in_seconds} seconds for next try.")
                    tries += 1
                    time.sleep(wait_time_in_seconds)            
        return wrapper
    return check

def measure_runtime(func):
    #decorator function, returns the total runtime of a decorated function or method.
    def wrapper(*args, **kwargs):
        starttime = time.time()
        result_of_function = func(*args, **kwargs)
        logging.info(f"{func.__name__}() function took " + str(time.time()-starttime) + " seconds to run")
        return result_of_function
    return wrapper

def split_custom_char(string, split_char, occurence):
# rnd_str = 'Https://doe-maar-iets.net/een-container-of-iets/folder-dan/file-naam.xlsx'
# tst = split_custom_char(rnd_str,'/', 3)
# print(tst)
# >> Https://doe-maar-iets.net

    if string.count(split_char) == 1:
        return string.split(split_char)[0]
    return split_char.join(string.split(split_char, occurence)[:occurence])

def getcurrent_datetime():
      now = datetime.now()
      return now.astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%Y/%m/%d %H:%M:%S")

def getcurrent_year():
      now = datetime.now()
      return now.astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%Y")

def getcurrent_month():
      now = datetime.now()
      return now.astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%m")      

def getcurrent_day():
      now = datetime.now()
      return now.astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%d")      

def getcurrent_hour():
      now = datetime.now()
      return now.astimezone(pytz.timezone('Europe/Amsterdam')).strftime("%H")     

def gettime_epoch():
    return int(time.time())

def encode_data(d):
    json_data = json.loads(d)
    logging.debug('Type: %s', type(json_data))
    s = json.dumps(json_data)
    enc = s.encode()  # utf-8 by default
    payload = base64.encodestring(enc)
    logging.debug('encoded: %s', payload)
    return payload
