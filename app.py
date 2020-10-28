#import depencies
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask
from flask import Flask, jsonify
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite") #connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
    return (
        f"<h1>Welcome to the Honolulu, Hawaii Weather Analysis!</h1><br/>"
        f"<h2>Please use the following routes:</h2><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>")

# Precipitation API
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    prcp = {date: prcp for date, prcp in last_year}

    return jsonify(prcp)

# Stations API
@app.route("/api/v1.0/stations")
def stations():
    station_count = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

    return jsonify(station_count)
        

# Temperature Observations API
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_ly = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').all()

    tobs = list(np.ravel(tobs_ly))

    return jsonify(tobs)

# Start date API
@app.route("/api/v1.0/<start>")
def temp_start(start):
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    temp = list(np.ravel(query))

    return jsonify(temp)

# Start/End date API
@app.route("/api/v1.0/<start>/<end>")
def date_range(start, end):
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temp =list(np.ravel(query))

    return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)
