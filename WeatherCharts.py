import WeatherStore
from kivy.logger import Logger
from time import gmtime, strftime
import pygal
from pygal.style import DarkStyle, DarkGreenBlueStyle
from random import randint, random,sample

class WeatherCharts:
    def __init__(self,weatherStore,config):
        Logger.info("WeatherCharts")
        self.ws = weatherStore
        self.config = config
        
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
