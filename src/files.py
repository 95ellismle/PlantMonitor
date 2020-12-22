import os
import pickle
import pandas as pd
import datetime
import sqlite3


datetime_format = "%Y/%m/%d %H:%M:%S"



def insert_into_db(dTime, reading, error, table, db_filepath):
   """ 
   Will insert some data into the sqlite3 db.

   Inputs:
      * dTime <datetime.datetime|str> => The datetime of reading
      * reading <float> => The reading from the sensor
      * error <float> => The error associated with the reading
		* table <str> => The name of the table within the sqlite3 db
		* db_filepath <str> => The database filepath.
   """
   db = sqlite3.connect(db_filepath)

   if type(dTime) == type(datetime.datetime.now()):
      dTime = datetime.datetime.strftime(dTime, datetime_format)
   
   elif type(dTime) != str:
      print("Can't insert data I don't understand the type for 'dTime'")
      raise TypeError

   query = "INSERT INTO " + table + " (DateTime,SensorValue,ReadingError) "
   query += 'VALUES ("%s",%.12f,%.12f)' % (dTime, reading, error)
   
   db.execute(query)
   db.commit()

   db.close()


def write_to_log(msg, log_file):
   """
   Will write a message to a log file in a standardised format.

   Inputs:
      * msg <str> => The message to write
      * log_file <str> => The filepath of the log file.
   """
   now = datetime.datetime.now()
   with open(log_file, 'a') as f:
      f.write("%s| %s\n" % (datetime.datetime.strftime(now, datetime_format),
                          msg))


def write_to_csv(fp, data):
    """
    Will save the data from the moisture pin to a file.

    If the file exists the data will be appended, if not it
    will be created and data written.

    Inputs:
        * fp <str> => The filepath to save the data
        * data <dict> => keys: column titles, values: data values.

    Outputs:
        None
    """
    append = True if os.path.isfile(fp) else False

    # Create dir if not there
    fold = '/'.join(fp.split('/')[:-1])
    if fold and not os.path.isdir(fold): os.makedirs(fold)

    # Create the data string to write
    cols = tuple(map(str, data.keys()))
    if not cols: return

    s = "" if append else','.join(cols) + "\n"
    for i in range(len(data[cols[0]])):
        for col in cols[:-1]:
            s += str(data[col][i]) + ","
        s += str(data[cols[-1]][i])
        s += "\n"

    # Write the data
    with open(fp, 'a') as f:
        f.write(s)


def read_csv(fp):
   """
   Will read a csv and return the pd.DataFrame containing the data.

   Inputs:
      * fp <str> => The filepath to the data file.

   Outputs:
      <pandas.DataFrame> The data from the file.
   """
   if not os.path.isfile(fp): return pd.DataFrame({})

   return pd.read_csv(fp)


def read_config(config_file):
    """ 
    Will read a configuration file and return the dict data.

    Inputs:
        * config_file <str> => The filepath of the configuration file.

    Outputs:
        <dict> The configuration data
    """
    if not os.path.isfile(config_file):
        return {}

    with open(config_file, 'rb') as f:
        return pickle.load(f)


def write_config(config_file, data):
    """ 
    Will write the configuration data as a config file.

    This will basically just pickle a dictionary.

    Inputs:
        * config_file <str> => The filepath of the configuration file.
        * data <dict> => The data to be stored.

    Outputs:
        None
    """
    # Create dir if not there
    fold = '/'.join(config_file.split('/')[:-1])
    if fold and not os.path.isdir(fold): os.makedirs(fold)
    # Write config data
    with open(config_file, 'wb') as f:
        pickle.dump(data, f)


def set_config(config, param, value, config_file):
    """ 
    Will set the configuration data and then write the file

    Inputs:
        * config <dict> => The dictionary to alter
        * param <dict > => The name of the param to set
        * value <*> => The value of the parameter
        * config_file <str> => The filepath of the config file.

    Outputs:
        None
    """
    config[param] = value
    write_config(config_file, config)

