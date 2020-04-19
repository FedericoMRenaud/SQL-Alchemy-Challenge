#Dependencies
import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
#Flask
app = Flask(__name__)

#Flask Routes

@app.route("/")
def home():
    "List of all routes."
    return(
        f"Available Routes: <br><br/>"

        f"/api/v1.0/precipitation<br>"

        f"/api/v1.0/stations<br/>"

        f"/api/v1.0/tobs<br>"

        f"/api/v1.0/<start><br/>"
        
        f"/api/v1.0/<start>/<end><br><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    query_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-05-16", 
        Measurement.date <= "2017-05-16").\
        all()
    precipitation_dict = [query_results]

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    stations_ds = session.query(Measurement.station, func.count(Measurement.station)).\
                           group_by(Measurement.station).\
                           order_by(func.count(Measurement.station).desc())


    station_list = list(stations_ds)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    """query for the dates and temperature observations from a year from the last data point"""

    query_results = session.query(Measurement.date,  Measurement.tobs).\
                filter(Measurement.date >= '2016-08-16').\
                    order_by(Measurement.date).all()

    tobs_ls = list(query_results)
    return jsonify(tobs_ls)

@app.route("/api/v1.0/<start>")
def temperature_given_start_date(start, end):

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""

    temp_func = session.query(func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()


    return jsonify(temp_func)


if __name__ == '__main__':
    app.run(debug=True)

