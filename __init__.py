from configparser import ConfigParser
import os

parser = ConfigParser()
metadataFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata.ini")
parser.read(metadataFile)

__version__ = parser["Version"]["VERSION"]
