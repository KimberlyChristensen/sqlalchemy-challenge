import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
	f"/api/v1.0/stations<br/>"
	f"/api/v1.0/tobs<br/>"
	f"/api/v1.0/<start><br/>"
	f"/api/v1.0/<start>/<end><br/>"
	
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using 'date' as the key and 'prcp' as the value"""
    # Query precipitation
    first_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).group_by(Measurement.date)\
    .order_by(Measurement.date).filter(Measurement.date>first_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of observations
    precipitation = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        precipitation.append(measurement_dict)
    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset"""
    # Query stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) for the previous year"""
    #  Query the dates and temperature observations of the most active station for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').all()

    session.close()

    tobs_list = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""  
    #  When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date
 
    # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
    # and return the minimum, average, and maximum temperatures for that range of dates

    def calc_temps(start):
        """TMIN, TAVG, and TMAX for a list of dates.  
        Args:
            start (string): A date string in the format %Y-%m-%d
            end (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        """
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
        
    session.close()

    temps_data=calc_temps(start)
    temps_start=[]    
    for tmin, tavg, tmax in temps_data:
        start_dict = {}
        start_dict["tmin"] = tmin
        start_dict["tavg"] = tavg
        start_dict["tmax"] = tmax
        temps_start.append(start_dict)

    return jsonify(temps_start)
    
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range."""  
    #  When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
 
    # This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
    # and return the minimum, average, and maximum temperatures for that range of dates

    def calc_temps(start, end):
        """TMIN, TAVG, and TMAX for a list of dates.  
        Args:
            start (string): A date string in the format %Y-%m-%d
            end (string): A date string in the format %Y-%m-%d
        
        Returns:
            TMIN, TAVE, and TMAX
        """
        return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
    session.close()

    temps_data_end=calc_temps(start, end)
    temps_start_end=[]    
    for tmin, tavg, tmax in temps_data_end:
        start_end_dict = {}
        start_end_dict["tmin"] = tmin
        start_end_dict["tavg"] = tavg
        start_end_dict["tmax"] = tmax
        temps_start_end.append(start_end_dict)

    return jsonify(temps_start_end)

if __name__ == '__main__':
    app.run(debug=True)
