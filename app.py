#T.BRADFORD
#July 2021

import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_scores = list(np.ravel(prcp_scores))

    return jsonify(prcp_scores)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    station_activity = (session.query(Measurement.station, func.count(Measurement.station))
        .group_by(Measurement.station)
        .order_by(func.count(Measurement.station).desc())
        .all())

    session.close()

    # Convert list of tuples into normal list
    station_activity = list(np.ravel(station_activity))

    return jsonify(station_activity)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query
    lowest_temp = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.station == "USC00519281").all()

    highest_temp = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.station == "USC00519281").all()

    average_temp = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.station == "USC00519281").all()

    session.close()

    # Convert list of tuples into normal list
    lowest_temp = list(np.ravel(lowest_temp))

    highest_temp = list(np.ravel(highest_temp))

    average_temp = list(np.ravel(average_temp))

    return jsonify(lowest_temp,highest_temp,average_temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start_end(start,end = None):
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query
    #start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    #end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    if not end:
        #start1 = session.query(*sel).filter(dt.datetime.strftime("%m-%d", Measurement.date) == start_date).all() 
        start1 = session.query(*sel).filter(Measurement.date >= start).all
        start1 = list(np.ravel(start1))
        return jsonify(start1)

    #start2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start2 = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <=end).all
    session.close()
    start2 = list(np.ravel(start2))
    return jsonify(start2)



if __name__ == '__main__':
    app.run(debug=True)
