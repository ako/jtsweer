from kivy.logger import Logger
import pandas as pd
from pandas import DataFrame
from StringIO import StringIO
import os
import sqlalchemy
from sqlalchemy import create_engine, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select, and_
from pytz import UTC, timezone
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import Table, Column, Numeric, DateTime, String, MetaData, Boolean
from math import pi, isnan
from decimal import Decimal
 
class WeatherStore:
    def __init__(self,config):
        Logger.info("WeatherStore")
        #self.datastore = pd.DataFrame()
        self.config = config
        self.engine = create_engine('mysql://{0}:{1}@localhost/{2}'.\
            format(self.config.get('Database','jtsdb_user'),\
                   self.config.get('Database','jtsdb_password'),\
                   self.config.get('Database','jtsdb_dbname')),echo=True)
        self.metadata = MetaData()
        self.observations = Table('observations',self.metadata,
                Column('timestamp',DateTime,nullable=False),
                Column('name',String(50),nullable=False),
                Column('source',String(50),nullable=False),
                Column('valueNum',Numeric(10,2),nullable=True),
                Column('valueString',String(50),nullable=True),
                Column('isForecast',Boolean,nullable=True),
                PrimaryKeyConstraint('timestamp', 'name', name='mytable_pk')
            )
        self.metadata.create_all(self.engine)
        
    def addObservation(self, timestamp, name, value, source):
        Logger.info("addObservation: {},{},{}".format(timestamp,name,value))
        if timestamp is not None and timestamp is not '':
            conn = self.engine.connect()
            try:
                Logger.info("value = >{}<".format(value) )
                if value in ("NA","--","N/A") :
                    val = Decimal()
                else:
                    val = Decimal(value)
                obsInsert = self.observations.insert().values(timestamp=timestamp.tz_convert(None),name=name,source=source,valueNum=val,valueString=None,isForecast=False)
                result = conn.execute(obsInsert)
            except SQLAlchemyError as e:
                Logger.warn("Error {}".format(e))
                pass
        #self.logDatastore()

    def addObservationString(self, timestamp, name, value, source):
        Logger.info("addObservationString: {},{},{}".format(timestamp,name,value))
        if timestamp is not None and timestamp is not '':
            conn = self.engine.connect()
            try:
                obsInsert = self.observations.insert().values(timestamp=timestamp.tz_convert(None),name=name,source=source,valueNum=None,valueString=value,isForecast=False)
                result = conn.execute(obsInsert)
            except SQLAlchemyError as e:
                Logger.warn("Error {}".format(e))
                pass
    
    def dumpDatastore(self,dt):
        Logger.info("dumpDatastore")
    
    def restoreDatastore(self):
        Logger.info("restoreDatastore")
       
    def getLatestObservation(self,name):
        Logger.info("getLatestObservation {}".format(name))
        conn = self.engine.connect()
        s = select([self.observations.c.valueNum]).\
            where(and_(self.observations.c.name == name,self.observations.c.timestamp <= pd.Timestamp.now('CET').tz_convert(None),self.observations.c.isForecast == False)).\
            order_by(desc(self.observations.c.timestamp))
        result = conn.execute(s)
        row = result.fetchone()
        result.close()
        return row['valueNum']

    def getLatestObservationString(self,name):
        Logger.debug("getLatestObservation {}".format(name))
        conn = self.engine.connect()
        s = select([self.observations.c.valueString]).\
            where(and_(self.observations.c.name == name,self.observations.c.timestamp <= pd.Timestamp.now('CET').tz_convert(None),self.observations.c.isForecast == False)).\
            order_by(desc(self.observations.c.timestamp))
        result = conn.execute(s)
        row = result.fetchone()
        result.close()
        return row['valueString']

    def loggerDataframe(self,dataframe):
        dfTxt = StringIO()
        dataframe.to_string(dfTxt)
        Logger.info(dfTxt.getvalue())
        dfTxt.close()        
