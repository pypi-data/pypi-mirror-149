import os

from configparser import ConfigParser
from NGPIris import WD

from distutils.sysconfig import get_python_lib

def get_config():
    config = ConfigParser()

    foundpath = False
    joiner = "" 
    while not foundpath:
        joiner = os.path.join(joiner, "..")
        config_path=os.path.join(WD, joiner, 'NGPIris', 'config.ini')
        foundpath = os.path.isfile(config_path)

    config.read(config_path)

    return config
