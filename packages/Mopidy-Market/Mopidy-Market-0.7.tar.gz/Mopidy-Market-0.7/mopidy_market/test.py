import configparser
import os
config = configparser.ConfigParser()
from os.path import expanduser
home = expanduser("~")
configfile = os.path.join(home,'.config/mopidy/mopidy.conf')

config.read(configfile)
print(config.sections())
