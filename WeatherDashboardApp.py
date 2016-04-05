import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.graphics.svg import Svg
from time import gmtime, strftime
from pygal.style import DarkStyle, DarkGreenBlueStyle
from random import randint, random,sample
from math import pi
import matplotlib.pyplot as plt
import numpy as np
import pygal                                                       # First import pygal
import requests
import json
import ConfigParser, os
from WeatherStore import WeatherStore
from WeatherDataImport import WeatherDataImport
      
class WindCharts:
    def generateWindChart(self):
        Logger.info("> generateWindChart " + strftime("%Y-%m-%d %H:%M:%S"))
        plt.figure(figsize=[6,6])
        x = np.arange(0,100,0.00001)
        y = x*np.sin(2*pi*x)
        plt.plot(y)
        plt.axis('off')
        plt.gca().set_position([0, 0, 1, 1])
        Logger.info("  generateWindChart " + strftime("%Y-%m-%d %H:%M:%S"))
        plt.savefig("test.png")
        Logger.info("< generateWindChart" + strftime("%Y-%m-%d %H:%M:%S"))

    def generateWindChartPygal(self):
        Logger.info("> generateWindChartPygal " + strftime("%Y-%m-%d %H:%M:%S"))
        bar_chart = pygal.Bar(style=DarkGreenBlueStyle)
        bar_chart.add('Fibonacci', sample(xrange(100),10))
        bar_chart.render_to_png('bar_chart.png')
        Logger.info("< generateWindChartPygal " + strftime("%Y-%m-%d %H:%M:%S"))

    def generateTempSparkline(self):
        Logger.info("> generateTempSparkline " + strftime("%Y-%m-%d %H:%M:%S"))
        bar_chart = pygal.Line(style=DarkGreenBlueStyle)
        bar_chart.add('', sample(xrange(100),10))
        bar_chart.render_sparkline()
        bar_chart.render_to_png('temp_sparkline.png')
        Logger.info("< generateWindChartPygal " + strftime("%Y-%m-%d %H:%M:%S"))
                 
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
    
    def refreshDisplayValues(self,dt):
        Logger.info("refreshDisplayValues")
        self.windKph = int(self.ws.getLatestObservation("wind_kph"))
        self.tempC = int(self.ws.getLatestObservation("temp_c"))
        self.windKnt = int(self.ws.getLatestObservation("wind_knt"))
        self.windDegrees = int(self.ws.getLatestObservation("wind_degrees"))
        self.tempFeel = "Voelt als {}".format(self.ws.getLatestObservation("feelslike_c"))
        self.Dew = "Dauwpunt {}".format(self.ws.getLatestObservation("dewpoint_c"))
        
    def __init__(self, **kwargs):
        super(WeatherDashboardApp,self).__init__(**kwargs)
        Logger.info("WeatherDashboardApp")
        config = ConfigParser.ConfigParser()
        config.read([os.path.expanduser('~/.jtsweer.cfg')])
        self.ws = WeatherStore(config)
        self.ws.restoreDatastore()
        self.wdi = WeatherDataImport(self.ws,config)
        Clock.schedule_interval(self.wdi.refreshGetij, 3600)
        Clock.schedule_interval(self.wdi.refreshScheveningenActueel, 300)
        Clock.schedule_interval(self.ws.dumpDatastore, 300)
        self.wdi.refreshGetij(0)
        self.wdi.refreshScheveningenActueel(0)
        self.ws.dumpDatastore(0)
        Clock.schedule_interval(self.refreshDisplayValues,5)
        
    def build(self):
        return CurrentWeather()
        
    def quitApp(self):
        Logger.info("Quitting app")
        App.get_running_app().stop()        
        
class CurrentWeather(GridLayout):
    myTime = StringProperty(strftime("%Y-%m-%d %H:%M:%S"))
    windKph = NumericProperty(-42)

    def refreshCharts(self,dt):
        Logger.info("refreshCharts: ")
        windCharter = WindCharts()
        windCharter.generateWindChartPygal()
        windCharter.generateTempSparkline()
        self.ids.windChart.ids.image.reload()

    def setClock(self,dt):
        Logger.info("setClock: ")
        self.myTime = strftime("%Y-%m-%d %H:%M:%S")
    
    def __init__(self, **kwargs):
        super(CurrentWeather,self).__init__(**kwargs)
        self.ids.tempTile.tileValue = "-1"
        Clock.schedule_interval(self.setClock, 1)
        Clock.schedule_interval(self.refreshCharts, 60)
        self.setClock(0)
        self.refreshCharts(0)
    
if __name__ in ('__main__'):
    WeatherDashboardApp().run()  