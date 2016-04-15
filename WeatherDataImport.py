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
from exceptions import ValueError, AttributeError

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
                self.ws.addObservation(pd.Timestamp(row['timestamp']).tz_localize('MET'),'getij',float(row['height']),'getij.rws.nl')
            except ValueError:
                Logger.info("oops")
                pass
            except AttributeError:
                Logger.info("oops")
                pass

    def loggerDataframe(self,dataframe):
        dfTxt = StringIO()
        dataframe.to_string(dfTxt)
        Logger.info(dfTxt.getvalue())
        dfTxt.close()

    def refreshOpenWeatherMap(self,dt):
        Logger.info("refreshOpenWeatherMap")
        owmKey = self.config.get('OpenWeatherMap','key')
        owmLongitude = self.config.get('OpenWeatherMap','longitude')
        owmLatitude = self.config.get('OpenWeatherMap','latitude')
        #
        # Get current weather
        #
        r = requests.get("http://api.openweathermap.org/data/2.5/weather?lon={}&lat={}&appid={}&units=metric".format(owmLongitude,owmLatitude,owmKey))
        actResponse = json.loads(r.text)
        print(json.dumps(actResponse,indent=4,sort_keys=True))
        source = "owm_the_hague"
        tempC = actResponse["main"]["temp"]
        observationTime = pd.to_datetime(actResponse["dt"],unit='s').tz_localize('utc')
        actWindMs = int(actResponse["wind"]["speed"])
        actWindKnt = int(actWindMs * 1.9438445)
        actWindDegrees = int(actResponse["wind"]["deg"])
        actPressure = int(actResponse["main"]["pressure"])
        actHumidity = int(actResponse["main"]["humidity"])
        self.ws.addObservation(observationTime,"temp_c",tempC,source)        
        self.ws.addObservation(observationTime,"wind_ms",actWindMs,source)        
        self.ws.addObservation(observationTime,"wind_knt",actWindKnt,source)        
        self.ws.addObservation(observationTime,"wind_degrees",actWindDegrees,source)        
        self.ws.addObservation(observationTime,"pressure_mb",actPressure,source)        
        self.ws.addObservation(observationTime,"relative_humidity",actHumidity,source)        
        #
        # Get 5 day forecast
        #
        #r = requests.get("http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&units=metric".format(owmLongitude,owmLatitude,owmKey))
        #actResponse = json.loads(r.text)
        #print(json.dumps(actResponse,indent=4,sort_keys=True))
        
    def refreshScheveningenActueel(self,dt):
        Logger.info("refreshScheveningenActueel: ")
        wuPars = {
        }
        wuKey = self.config.get('WeatherUnderground','key')
        wuCountry = self.config.get('WeatherUnderground','country')
        wuStation = self.config.get('WeatherUnderground','station')
        Logger.info("key: {}".format(wuKey))
        r = requests.get("http://api.wunderground.com/api/{}/conditions/q/{}/{}.json".format(wuKey,wuCountry,wuStation))
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
        actObservationTime2 = pd.Timestamp(actObservationTime)
        actPrecipitation1hr = actResponse["current_observation"]["precip_1hr_metric"]
        actPrecipitationToday = actResponse["current_observation"]["precip_today_metric"]
        actPressureMb = actResponse["current_observation"]["pressure_mb"]
        actRelativeHumidity = actResponse["current_observation"]["relative_humidity"]
        actVisibility = actResponse["current_observation"]["visibility_km"]
        self.ws.addObservation(actObservationTime2,"temp_c",actTempC,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"dewpoint_c",actDewpointC,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"feelslike_c",actFeelslikeC,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"windchill_c",actWindchillC,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"wind_kph",actWindKph,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"wind_knt",actWindKnt,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"wind_gust_kph",actWindGustKph,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"wind_gust_knt",actWindGustKnt,"wu_the_hague")        
        self.ws.addObservationString(actObservationTime2,"wind_dir",actWindDir,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"wind_degrees",actWindDegrees,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"precip_1hr_metric",actPrecipitation1hr,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"precip_today_metric",actPrecipitationToday,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"pressure_mb",actPressureMb,"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"relative_humidity",actRelativeHumidity.strip('%'),"wu_the_hague")        
        self.ws.addObservation(actObservationTime2,"visibility_km",actVisibility,"wu_the_hague")        
