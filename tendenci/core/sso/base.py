import time
import uuid

def get_random_id():
    #NOTE: It is very important that these random IDs NOT start with a number.
    random_id = '_' + uuid.uuid4().hex
    return random_id

def get_time_string(delta=0):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime(time.time() + delta))
