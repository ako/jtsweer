import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.graphics.svg import Svg
from time import gmtime, strftime
from math import pi, isnan
import matplotlib.pyplot as plt
import numpy as np
import pygal
import requests
import json
import ConfigParser, os
from WeatherStore import WeatherStore
from WeatherDataImport import WeatherDataImport
from WeatherCharts import WeatherCharts
from kivy.config import Config
                 
class TimeWidget(Widget):
    time = NumericProperty(42)
    
    def __init__(self, **kwargs):
        super(TimeWidget,self).__init__(**kwargs)
        
class WeatherDashboardApp(App):
    windKph = NumericProperty(0)
    tempC = NumericProperty(0)
    tempCLabel = StringProperty("Graden celcius")
    tempFeel = NumericProperty(-1)
    tempDew = NumericProperty(-1)
    tempSparkChart = StringProperty("bar_chart.png")
    summaryChart = StringProperty("")
    windKnt = NumericProperty(0)
    windDegrees = NumericProperty(0)
    windGustKnt = NumericProperty(0)
    humidity = NumericProperty(0)
    tileColor = StringProperty()
    
    def refreshCharts(self,dt):
        Logger.info("refreshCharts")
        self.wc.generateWindChartPygal()
        self.wc.generateTempSparkline()
        
    def refreshDisplayValues(self,dt):
        Logger.info("refreshDisplayValues")
        self.windKph = int(self.ws.getLatestObservation("wind_kph"))
        tempC = self.ws.getLatestObservation("temp_c")
        self.tempC = int(float(tempC if not isnan(tempC) else 0))
        windKnt = self.ws.getLatestObservation("wind_knt")
        self.windKnt = int(windKnt if not isnan(windKnt) else 0)
        windDegrees = self.ws.getLatestObservation("wind_degrees")
        self.windDegrees = int(float(windDegrees) if not isnan(windDegrees) else 0)
        self.tempFeel = int(float(self.ws.getLatestObservation("feelslike_c")))
        self.tempDew = int(self.ws.getLatestObservation("dewpoint_c"))
        self.windGustKnt = int(self.ws.getLatestObservation("wind_gust_knt"))
        self.humidity = int(self.ws.getLatestObservation("relative_humidity"))
        tmppath = self.appconfig.get('General','temppath')
        #tmppath = "/tmp"
        self.summaryChart = ""
        self.tempSparkChart = ""
        self.summaryChart = os.path.join(tmppath,'bar_chart.png')
        self.tempSparkChart = os.path.join(tmppath,"temp_sparkline.png")
        
    def __init__(self, **kwargs):
        super(WeatherDashboardApp,self).__init__(**kwargs)
        Logger.info("WeatherDashboardApp")
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '480')
        self.appconfig = ConfigParser.ConfigParser()
        self.appconfig.read([os.path.expanduser('~/.jtsweer.cfg')])
        self.ws = WeatherStore(self.appconfig)
        #self.ws.restoreDatastore()
        self.wdi = WeatherDataImport(self.ws,self.appconfig)
        self.wc = WeatherCharts(self.ws,self.appconfig)
        Clock.schedule_interval(self.wdi.refreshGetij, 3600)
        Clock.schedule_interval(self.wdi.refreshScheveningenActueel, 300)
        Clock.schedule_interval(self.wdi.refreshOpenWeatherMapActueel, 600)
        Clock.schedule_interval(self.wdi.refreshOpenWeatherMapForecast, 3600)
        #Clock.schedule_interval(self.ws.dumpDatastore, 300)
        self.wdi.refreshGetij(0)
        self.wdi.refreshScheveningenActueel(0)
        self.wdi.refreshOpenWeatherMapActueel(0)
        self.wdi.refreshOpenWeatherMapForecast(0)
        self.ws.dumpDatastore(0)
        Clock.schedule_interval(self.refreshDisplayValues,5)
        Clock.schedule_interval(self.refreshCharts,60)
        self.refreshCharts(0)
                
    def build(self):
        return CurrentWeather()
        
    def quitApp(self):
        Logger.info("Quitting app")
        App.get_running_app().stop()        
        
class CurrentWeather(BoxLayout):
    myTime = StringProperty(strftime("%Y-%m-%d %H:%M:%S"))

    def refreshCharts(self,dt):
        Logger.info("refreshCharts: ")
        self.ids.windChart.ids.image.reload()

    def setClock(self,dt):
        Logger.debug("setClock: ")
        self.myTime = strftime("%Y-%m-%d %H:%M:%S")
    
    def __init__(self, **kwargs):
        super(CurrentWeather,self).__init__(**kwargs)
        self.ids.tempTile.tileValue = "-1"
        Clock.schedule_interval(self.setClock, 1)
        self.setClock(0)
    
if __name__ in ('__main__'):
    WeatherDashboardApp().run()
    