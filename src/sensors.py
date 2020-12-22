import RPi.GPIO as GPIO
import time
import datetime
from collections import OrderedDict
import signal

import files
from sensor_config import *
import sensor_utils as utils
#import communications as comm


def exit_gracefully(signum, frame):
   """
   Will catch the SIGTERM signal and exti gracefully.
   """
   files.write_to_log("SIGTERM detected -exitting gracefully.", log_file)
   GPIO.cleanup()
   raise SystemExit

signal.signal(signal.SIGTERM, exit_gracefully)



files.write_to_log("""Starting sensor data collection. Params:
   * moisturePIN  = """ + str(moisturePIN) + """
   * config_file  = """ + str(config_file) + """ 
   * data_file    = """ + str(data_file) + """ 
   * read_timeout = """ + str(read_timeout) + """ 
   * reminder_point  = """ + str(reminder_point) + """ 
   * datetime_format = """ + str(datetime_format) + """ 
   * log_file        = """ + str(log_file) + """ 
   * db_filepath     = """ + str(db_filepath) + """ 
   * db_tableName    = """ + str(db_tableName) + """ 
   * sensor_read_timeout         = """ + str(sensor_read_timeout) + """
   * time_between_reading_bursts = """ + str(time_between_reading_bursts) + """ 
   * time_between_indiv_readings = """ + str(time_between_indiv_readings) + """ 
   * num_readings_each_burst     = """ + str(num_readings_each_burst) + """ 
""", log_file)
config = files.read_config(config_file)

data = OrderedDict()
while True:
    try:

       val, err = utils.getCleanMoistureVal(moisturePIN, num_readings_each_burst, time_between_indiv_readings)
       if val is None: 
           files.write_to_log("No reading taken -'getCleanMoistureVal' returned None. Not Fatal.", log_file)
           continue

       if err is None:
           files.write_to_log("No error calculated -'getCleanMoistureVal' returned None. Not Fatal", log_file)
           err = 1e6
   
       now = datetime.datetime.now()
       data['datetime'] = [datetime.datetime.strftime(now, datetime_format)]
       data['discharge_time_ivy'] = [val]
       data['discharge_time_ivy_err'] = [err]
       files.write_to_log("Reading at %s: %.3f +/- %.0g             " % (data['datetime'][0],
                                                                         val, err),
                          log_file)
   
       files.insert_into_db(now,
                            data['discharge_time_ivy'][0],
                            data['discharge_time_ivy_err'][0],
                            db_tableName,
                            db_filepath)
   
       # Sleep for 1/2 an hour
       time.sleep(time_between_reading_bursts)

    except KeyboardInterrupt as e:
      files.write_to_log("KeyboardInterrupt Detected -exitting.", log_file)
      break
    
    except Exception as e:
      files.write_to_log("Exception detected -exitting. Exception = %s" % (str(e)), log_file)
      break


GPIO.cleanup()

files.write_to_log("Ending sensor data collection", log_file)



#if val < 0.16 and not files.config.get('sent_mail', False):
#    comm.send_email("95ellismle@gmail.com", "Hi Matt,\n\nPlease remember to water the ivy today!\n\nBest,\n\nPlant Bot 1000",
#               "Ivy Watering Reminder")
#    files.set_config(config, 'sent_mail', True, config_file)

