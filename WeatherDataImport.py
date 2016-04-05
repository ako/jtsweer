import requests
import json
import WeatherStore
from kivy.logger import Logger
import datetime
from time import gmtime, strftime
from dateutil.parser import parse
import numpy as np
from StringIO import StringIO
from matplotlib.dates import strpdate2num
import pandas as pd
from exceptions import ValueError

class WeatherDataImport:
    
    def __init__(self,weatherStore,config):
        Logger.info("WeatherDataImport")
        self.ws = weatherStore
        self.config = config
        
    def refreshGetij(self,dt):
        Logger.info("refreshGetij: ")
        # http://getij.rws.nl/export.cfm?format=txt&from=02-04-2016&to=08-04-2016&uitvoer=1&interval=10&lunarphase=yes&location=SCHEVNGN&Timezone=MET_DST&refPlane=NAP&graphRefPlane=NAP
        getijPars = {
            'format' : 'txt',
            'from' : strftime("%d-%m-%Y"),
            'to' : strftime("%d-%m-%Y"),
            'uitvoer': 1,
            'interval': 10,
            'lunarphase': 'yes',
            'location': 'SCHEVNGN',
            'Timezone':'MET_DST',
            'refPlane':'NAP',
            'graphRefPlane':'NAP'
        }
        r = requests.get("http://getij.rws.nl/export.cfm",params=getijPars)
        Logger.info(r.text)
        dataFile = StringIO(r.text)
        df = pd.read_fwf(dataFile,widths=[17,6,3],names=['timestamp','height','unit'],skiprows=14)
        self.loggerDataframe(df.head())
        dataFile.close()
        for index, row in df.iterrows():
            try:
                self.ws.addObservation(row['timestamp'],'getij',float(row['height']))
            except ValueError:
                pass

    def loggerDataframe(self,dataframe):
        dfTxt = StringIO()
        dataframe.to_string(dfTxt)
        Logger.info(dfTxt.getvalue())
        dfTxt.close()

    def refreshScheveningenActueel(self,dt):
        Logger.info("refreshScheveningenActueel: ")
        wuPars = {
        }
        wuKey = self.config.get('WeatherUnderground','key')
        Logger.info("key: {}".format(wuKey))
        r = requests.get("http://api.wunderground.com/api/{}/conditions/q/{}/The_Hague.json".format(wuKey,"NL"))
        actResponse = json.loads(r.text)
        print(json.dumps(actResponse,indent=4,sort_keys=True))
        actTempC = actResponse["current_observation"]["temp_c"]
        actDewpointC = actResponse["current_observation"]["dewpoint_c"]
        actFeelslikeC = actResponse["current_observation"]["feelslike_c"]
        actWindchillC = actResponse["current_observation"]["windchill_c"]
        actWindKph = int(actResponse["current_observation"]["wind_kph"])
        actWindKnt = int(actWindKph / 1.852)
        actWindGustKph = int(actResponse["current_observation"]["wind_gust_kph"])
        actWindGustKnt = int(actWindGustKph / 1.852)
        actWindDir = actResponse["current_observation"]["wind_dir"]        
        actWindDegrees = actResponse["current_observation"]["wind_degrees"]        
        actObservationTime = actResponse["current_observation"]["observation_time_rfc822"]
        actObservationTime2 = parse(actObservationTime)
        actPrecipitation1hr = actResponse["current_observation"]["precip_1hr_metric"]
        actPrecipitationToday = actResponse["current_observation"]["precip_today_metric"]
        actPressureMb = actResponse["current_observation"]["pressure_mb"]
        actRelativeHumidity = actResponse["current_observation"]["relative_humidity"]
        actVisibility = actResponse["current_observation"]["visibility_km"]
        self.ws.addObservation(actObservationTime2,"temp_c",actTempC)        
        self.ws.addObservation(actObservationTime2,"dewpoint_c",actDewpointC)        
        self.ws.addObservation(actObservationTime2,"feelslike_c",actFeelslikeC)        
        self.ws.addObservation(actObservationTime2,"windchill_c",actWindchillC)        
        self.ws.addObservation(actObservationTime2,"wind_kph",actWindKph)        
        self.ws.addObservation(actObservationTime2,"wind_knt",actWindKnt)        
        self.ws.addObservation(actObservationTime2,"wind_gust_kph",actWindGustKph)        
        self.ws.addObservation(actObservationTime2,"wind_gust_knt",actWindGustKnt)        
        self.ws.addObservation(actObservationTime2,"wind_dir",actWindDir)        
        self.ws.addObservation(actObservationTime2,"wind_degrees",actWindDegrees)        
        self.ws.addObservation(actObservationTime2,"precip_1hr_metric",actPrecipitation1hr)        
        self.ws.addObservation(actObservationTime2,"precip_today_metric",actPrecipitationToday)        
        self.ws.addObservation(actObservationTime2,"pressure_mb",actPressureMb)        
        self.ws.addObservation(actObservationTime2,"relative_humidity",actRelativeHumidity)        
        self.ws.addObservation(actObservationTime2,"visibility_km",actVisibility)        
