import logging
import sys
from .bcolors import bcolors as bc
from copy import copy
from  .fifo import FIFOIO

class CustomFormat(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def format(self, record):
        colors = [bc.ENDC,bc.OKBLUE,bc.OKGREEN,bc.WARNING,bc.Default,bc.FAIL,bc.OKBLUE,"\t","\n"]
        record = copy(record)
        record.msg = record.msg.strip()
        for x in colors:
            record.msg = record.msg.replace(x,"")
        return super().format(record)
def setup_logging (log_path):
    # set up logging to file - see previous section for more details
    # define a Handler which writes INFO messages or higher to the sys.stderr
    logger = logging.getLogger()
    custom_format = CustomFormat(fmt='%(asctime)s | %(name)s | %(threadName)s | %(levelname)s | %(message)s',datefmt='%m-%d %H:%M')
    file_log = logging.FileHandler(f"{str(log_path)}/meraki-tools.log",mode='w')
    file_log.setLevel(logging.WARNING)
    file_log.setFormatter(custom_format)
    logger.addHandler(file_log)
    
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)s | %(threadName)s | %(levelname)s | %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.addHandler(console)

def server_status_log():
    logger = logging.getLogger()
    log_capture_string = FIFOIO(256)
    format = CustomFormat(fmt='%(asctime)s | %(name)s | %(threadName)s | %(levelname)s | %(message)s',datefmt='%m-%d %H:%M')
    to_string = logging.StreamHandler(log_capture_string)
    to_string.setFormatter(format)
    to_string.setLevel(logging.INFO)
    to_string.name = "log_capture_string"
    logger.addHandler(to_string)
    return  log_capture_string
    


