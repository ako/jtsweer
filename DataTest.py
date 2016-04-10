import pandas as pd
from pandas import DataFrame
import ConfigParser, os
from kivy.logger import Logger

config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.jtsweer.cfg')])
tmppath = config.get('Data','temppath')
datastore = pd.DataFrame().from_csv(os.path.join("test","observations.csv"))
