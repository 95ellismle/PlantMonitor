import RPi.GPIO as GPIO
import time
import datetime
from collections import OrderedDict
import numpy as np
import signal

import files
import communications as comm

GPIO.setmode(GPIO.BCM)

moisturePIN  = 4 
sensor_read_timeout = 600  # 10 mins
config_file  = "config/config.params"
data_file    = "data/moisture_data.csv"
read_timeout = 3600
reminder_point = 0.16
datetime_format = "%Y/%m/%d %H:%M:%S"
log_file = "sensor.log"
db_filepath = "data/test.db"
#db_filepath = "data/test.db"
db_tableName = "IvyMoisture"

time_between_reading_bursts = 60  #1800 # 1/2 hour
time_between_indiv_readings = 10 # 300 # 5 mins
num_readings_each_burst = 12
