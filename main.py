from flask import Flask, jsonify, render_template, Response, g
import datetime
import numpy as np
import random
import sqlite3

from src import files


app = Flask(__name__)


#db_file = "data/SensorData.db"
db_file = "data/test.db"
datetime_format = "%Y/%m/%d %H:%M:%S"
table_name = "IvyMoisture"


def get_moisture_data(end_date=False, start_date=False):
   """
   Will return the jsonified csv moisture data.

   Inputs:
      * start_date <datetime.datetime> => The first date to request data from
      * end_date <datetime.datetime>   => The last date to request data from
   """
   if end_date is False:   end_date   = datetime.datetime.now()
   if start_date is False: start_date = end_date - datetime.timedelta(weeks=4)

   conn = sqlite3.connect(db_file)
   curr = conn.cursor()
   startT_str = datetime.datetime.strftime(start_date, datetime_format)
   endT_str = datetime.datetime.strftime(end_date, datetime_format)
   query = 'SELECT * FROM %s WHERE DateTime >= "%s" AND DateTime <= "%s"' % (
                      table_name,            startT_str,          endT_str)
   curr.execute(query)
   rows = np.array(curr.fetchall())
   if len(rows) == 0: 
      return {'datetime': [],
              'discharge_time_ivy': [],
              'discharge_time_ivy_err': [],}
   
   cvtTime = lambda t: t.replace("/", "-")
   data = {
         'datetime': list(map(cvtTime, rows[:, 1])),
         'discharge_time_ivy': list(map(float, rows[:, 2])),
         'discharge_time_ivy_err': list(map(float, rows[:, 3])),
          }

   conn.close()
   return data


@app.route("/")
def home():
     data = get_moisture_data()
     now = datetime.datetime.now()
     return render_template("index.html", data=data, now=now)


@app.route("/get_data")
def moisture_data():
   return Response(get_moisture_data().to_dict(orient="list"), mimetype="text/event-stream")

@app.route("/health.json")  
def health():
    return jsonify({"status": "UP"}), 200   


if __name__ == "__main__":
    app.run(                             )
#            debug=True,
#            TEMPLATES_AUTO_RELOAD=True,
#            FLASK_DEBUG=1,
#            )
