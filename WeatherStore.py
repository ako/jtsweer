from kivy.logger import Logger
import pandas as pd
from pandas import DataFrame
from StringIO import StringIO

class WeatherStore:
    def __init__(self,config):
        Logger.info("WeatherStore")
        self.datastore = pd.DataFrame()
        self.config = config
        
    def addObservation(self, timestamp, name, value):
        Logger.info("addObservation: {},{},{}".format(timestamp,name,value))
        if timestamp is not None:
            observation = pd.DataFrame({'name':name,'value':value},index=[pd.Timestamp(timestamp, tz='Europe/Amsterdam')])
            self.datastore = self.datastore.append(observation)
            Logger.info("addObservation - timestamp: {}".format(observation))
        #self.logDatastore()
    
    def dumpDatastore(self,dt):
        Logger.info("dumpDatastore")
        # csvOut = StringIO()
        # self.datastore.tail(10).to_csv(csvOut)
        # Logger.info(csvOut.getvalue())
        # csvOut.close()
        # Logger.info("count: {}".format(self.datastore.count()))
        self.datastore.to_csv("observations.csv",header=['name','value'])
    
    def restoreDatastore(self):
        Logger.info("restoreDatastore")
        try:
            self.datastore = pd.DataFrame().from_csv("observations.csv")
        except Exception:
            pass
        #self.datastore.reset_index().drop_duplicates(subset=['index','name'],take_last=True,inplace=True).set_index('index')
        #self.datastore.groupby([DF.index,)
        
    def getLatestObservation(self,name):
        Logger.info("getLatestObservation {}".format(name))
        namedf = self.datastore.loc[self.datastore['name'] == name]
        self.loggerDataframe(namedf)
        namedf = namedf.truncate(after=pd.to_datetime('now'))
        for index, row in namedf.iterrows():
            return row['value']        

    def loggerDataframe(self,dataframe):
        dfTxt = StringIO()
        dataframe.to_string(dfTxt)
        Logger.info(dfTxt.getvalue())
        dfTxt.close()        