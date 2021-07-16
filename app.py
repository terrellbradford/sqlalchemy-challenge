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
        f"/api/v1.0/<start><br/>"
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


def start_end(start):

#    # Create our session (link) from Python to the DB
    session = Session(engine)

 
    # Query
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = session.query(*sel).filter(Measurement.date >= start).all()

    session.close()

    # Append data to empty dictionary then append dictionary to empty list
    start_date = []
    for min, avg, max in results:
        start_date_dict = {}
        start_date_dict[f"The Minimum Temperature on {start} was"] = min
        start_date_dict[f"The Average Temperature on {start} was"] = avg
        start_date_dict[f"The Maximum Temperature on {start} was"] = max
        start_date.append(start_date_dict) 

    return jsonify(start_date)


@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
  
    # Append data to empty dictionary then append dictionary to empty list
    end_date = []
    for min, avg, max in results:
        end_date_dict = {}
        end_date_dict[f"The Minimum Temperature from {start} through {end} was"] = min
        end_date_dict[f"The Average Temperature from {start} through {end} was"] = avg
        end_date_dict[f"The Maximum Temperature from {start} through {end} was"] = max
        end_date.append(end_date_dict) 
    
    return jsonify(end_date)

if __name__ == '__main__':
    app.run(debug=True)
