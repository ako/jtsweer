#!/bin/bash

export DISPLAY=:0.
export JTSWEER_HOME=$(dirname $(realpath $0))
cd $JTSWEER_HOME
echo "basedir: $JTSWEER_HOME"
python WeatherDashboardApp.py
