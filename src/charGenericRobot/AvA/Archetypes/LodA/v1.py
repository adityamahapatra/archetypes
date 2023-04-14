import sys

# Temporary arrangement. Installation path would be configured in production.
sys.path.append("/home/aditya/Dev/projects")

# Third-party library imports.
from dotenv import load_dotenv
import requests
from pandas import DataFrame
import numpy

# Internal library imports.
from componentLibrary.src.charOptimusPrime.arm import v1 as arm
from componentLibrary.src.charOptimusPrime.leg import v2 as leg
from componentLibrary.src.charMpcHuman.spine import v3 as spine


def specs():
    pass


def build():
    pass
