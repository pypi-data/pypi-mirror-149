import logging
import os
from datetime import datetime

logformat =  logging.Formatter("[%(asctime)s] - %(levelname)s: %(message)s")

# File work directory
WD = os.path.dirname(os.path.realpath(__file__))
TIMESTAMP = datetime.now().strftime("%y%m%d-%H%M%S")

# Initialize log
log = logging.getLogger("main_log")
log.setLevel(logging.DEBUG)
#Streamlog
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logformat)
log.addHandler(ch)
