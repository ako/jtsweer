from kivy.logger import Logger
import pandas as pd
from pandas import DataFrame
from StringIO import StringIO
import os
import sqlalchemy
from sqlalchemy import create_engine
from pytz import UTC
from pytz import timezone

class WeatherStore:
    def __init__(self,config):
        Logger.info("WeatherStore")
        self.datastore = pd.DataFrame()
        self.config = config
        self.engine = create_engine('mysql://{0}:{1}@localhost/{2}'.\
            format(self.config.get('Database','jtsdb_user'),\
                   self.config.get('Database','jtsdb_password'),\
                   self.config.get('Database','jtsdb_dbname')))
        
    def addObservation(self, timestamp, name, value):
        Logger.info("addObservation: {},{},{}".format(timestamp,name,value))
        if timestamp is not None and timestamp is not '':
            observation = pd.DataFrame({'name':name,'valueNum':value,'valueString':None},index=[timestamp.tz_convert(None)])
            self.datastore = self.datastore.append(observation)
            Logger.info("addObservation - timestamp: {}".format(observation))
            observation.to_sql("observations",self.engine,flavor='mysql',if_exists='append',dtype={'index': sqlalchemy.types.DateTime})
        #self.logDatastore()

    def addObservationString(self, timestamp, name, value):
        Logger.info("addObservationString: {},{},{}".format(timestamp,name,value))
        if timestamp is not None and timestamp is not '':
            observation = pd.DataFrame({'name':name,'valueNum':None,'valueString':value},index=[timestamp.tz_convert(None)])
            self.datastore = self.datastore.append(observation)
            Logger.info("addObservation - timestamp: {}".format(observation))
            observation.to_sql("observations",self.engine,flavor='mysql',if_exists='append',dtype={'index': sqlalchemy.types.DateTime})
        #self.logDatastore()
    
    def dumpDatastore(self,dt):
        Logger.info("dumpDatastore")
        # csvOut = StringIO()
        # self.datastore.tail(10).to_csv(csvOut)
        # Logger.info(csvOut.getvalue())
        # csvOut.close()
        # Logger.info("count: {}".format(self.datastore.count()))
        tmppath = self.config.get('Data','temppath')
        self.datastore.to_csv(os.path.join(tmppath,"observations.csv"),header=['name','valueNum','valueString'])
    
    def restoreDatastore(self):
        Logger.info("restoreDatastore")
        try:
            tmppath = self.config.get('Data','temppath')
            self.datastore = pd.DataFrame().from_csv(os.path.join(tmppath,"observations.csv"))
            self.datastore =  self.datastore.sort().drop_duplicates()    
        except Exception as e:
            Logger.warn("Failed to read datastore: {0}".format(e.strerror))
            pass
        #self.datastore = self.datastore.groupby([self.datastore.index,'name'])
        #self.loggerDataframe(self.datastore.reset_index())
        #self.datastore.drop_duplicates(subset=[self.datastore.index,'name'],take_last=True,inplace=True).set_index('index')
        #self.datastore.groupby([DF.index,)
        
    def getLatestObservation(self,name):
        Logger.debug("getLatestObservation {}".format(name))
        ds1 = self.datastore.sort().drop_duplicates()
        val = ds1[ds1['name'] == name].sort(
                ascending=[0]).truncate(
                after=pd.Timestamp.now('CET')).sort(
                ascending=False)[:1]
        return val['valueNum']

    def getLatestObservationString(self,name):
        Logger.debug("getLatestObservation {}".format(name))
        ds1 = self.datastore.sort().drop_duplicates()
        val = ds1[ds1['name'] == name].sort(
                ascending=[0]).truncate(
                after=pd.Timestamp.now('CET')).sort(
                ascending=False)[:1]
        return val['valueString']

    def loggerDataframe(self,dataframe):
        dfTxt = StringIO()
        dataframe.to_string(dfTxt)
        Logger.info(dfTxt.getvalue())
        dfTxt.close()        
