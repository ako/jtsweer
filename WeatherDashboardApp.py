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
from math import pi
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
    tempFeel = StringProperty("Gevoelstemperatuur: -1C")
    tempDew = StringProperty("Dauwpunt: 2C")
    tempSparkChart = StringProperty("bar_chart.png")
    windKnt = NumericProperty(0)
    windDegrees = NumericProperty(0)
    
    def refreshCharts(self,dt):
        Logger.info("refreshCharts")
        self.wc.generateWindChartPygal()
        self.wc.generateTempSparkline()
        
    def refreshDisplayValues(self,dt):
        Logger.info("refreshDisplayValues")
        self.windKph = int(self.ws.getLatestObservation("wind_kph"))
        self.tempC = int(float(self.ws.getLatestObservation("temp_c")))
        self.windKnt = int(self.ws.getLatestObservation("wind_knt"))
        self.windDegrees = int(self.ws.getLatestObservation("wind_degrees"))
        self.tempFeel = "Voelt als {}".format(self.ws.getLatestObservation("feelslike_c"))
        self.Dew = "Dauwpunt {}".format(self.ws.getLatestObservation("dewpoint_c"))
        self.tempSparkChart = "bar_chart.png"
        
    def __init__(self, **kwargs):
        super(WeatherDashboardApp,self).__init__(**kwargs)
        Logger.info("WeatherDashboardApp")
        Config.set('graphics', 'width', '800')
        Config.set('graphics', 'height', '480')
        config = ConfigParser.ConfigParser()
        config.read([os.path.expanduser('~/.jtsweer.cfg')])
        self.ws = WeatherStore(config)
        self.ws.restoreDatastore()
        self.wdi = WeatherDataImport(self.ws,config)
        self.wc = WeatherCharts(self.ws,config)
        Clock.schedule_interval(self.wdi.refreshGetij, 3600)
        Clock.schedule_interval(self.wdi.refreshScheveningenActueel, 300)
        Clock.schedule_interval(self.ws.dumpDatastore, 300)
        self.wdi.refreshGetij(0)
        self.wdi.refreshScheveningenActueel(0)
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
        Logger.info("setClock: ")
        self.myTime = strftime("%Y-%m-%d %H:%M:%S")
    
    def __init__(self, **kwargs):
        super(CurrentWeather,self).__init__(**kwargs)
        self.ids.tempTile.tileValue = "-1"
        Clock.schedule_interval(self.setClock, 1)
        self.setClock(0)
    
if __name__ in ('__main__'):
    WeatherDashboardApp().run()
    