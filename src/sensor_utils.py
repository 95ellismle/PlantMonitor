import RPi.GPIO as GPIO
import time
import numpy as np

# I know this star import is naughty but it works well...
from sensor_config import *
import files




def timeToHigh(PIN):
    """ 
    Will time how long it takes to charge the capacitor.

    This time is proportional to the wetness of the medium the
    sensor is in.

    Inputs:
        * PIN <int> => The pin number the sensor is plugged into.

    Outputs:
        <float> Time taken to discharge
    """
    # Make sure the capacitor is discharged
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(1)

    # Start charging capacitor and measure time.
    GPIO.setup(PIN, GPIO.IN)
    start_time = time.time()
    while GPIO.input(PIN) == GPIO.LOW: 
       if (time.time() - start_time) > sensor_read_timeout: 
           files.write_to_log("Sensor took too long to read a value (more than %i seconds). Not fatal." % sensor_read_timeout, log_file)
           return None
       time.sleep(0.00001)
    end_time = time.time()

    # Keep capacaitor discharged
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, GPIO.LOW)

    return end_time - start_time


def getCleanMoistureVal(PIN, num_collections=12, time_between_collections=300):
    """ 
    Will get a reliable value for the moistness of the soil.

    Readings are taken with some time to rest between them. Any outliers are
    then removed from these readings and the mean of the
    remaining values is returned with a standard error.

    The outliers are removed by removing points that are 2 stddevs away from the
    mean and removing points that have jumped a large amount since the previous
    reading.
    
    Inputs: 
        * PIN <int> => The pin number the sensor is plugged into.
        * num_collections <int> OPTIONAL => The number of data points to collect and average over
        * time_between_collections <int|float> OPTIONAL => The time to wait between each data collection.

    Outputs:
        <float> Time taken to discharge
    """
    # Collect data
    data_points = []
    collection_number = 0 
    bad_point_count = 0 
    while (collection_number < num_collections):
        val = timeToHigh(PIN)
        if val is None:
            bad_point_count += 1
            continue
        if bad_point_count == 5:
            files.write_to_log("Tried 5 times to take reading from moisture sensor with function 'timeToHigh'. It returned 'None'. Fatal Error.", log_file)
            raise SystemExit("SensorError")
        data_points.append(timeToHigh(PIN))
        collection_number += 1

        time.sleep(time_between_collections)

    # Remove outliers if we have enough data.
    if num_collections > 5:
        data_points = np.array(data_points)
        data_grad = np.abs(np.gradient(data_points, time_between_collections))
        s = np.std(data_points)
        m = np.mean(data_points)
        stol = 2 
        gtol = 1e-5

        # Remove bad points
        good_point_mask = (data_grad < gtol) | ((data_points > m-(stol*s)) & (data_points < m+(stol*s)))
        clean_data = data_points[good_point_mask]
        files.write_to_log("All Data Readings: %s, Cleaned Data: %s" % ( 
                           ','.join(map(str, data_points)), ','.join(map(str, clean_data))),
                           log_file)

        if len(clean_data) <= 3:
            files.write_to_log("Data too noisy from sensor to take reasonable reading. Not Fatal.",
                               log_file)
            return None, data_points

        return np.mean(clean_data), np.std(clean_data) / np.sqrt(len(clean_data))

    # Return mean and average without cleaning if we don't take many points
    if num_collections > 1:
       return np.mean(data_points), np.std(data_points) / np.sqrt(len(data_points))

    # Return just mean if we have only 1 data point
    elif num_collections == 1:
       return data_points[0], None

