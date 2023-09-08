# Import Dependencies
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################
# Database Setup
#################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the DB
session = Session(engine)

#################################
# Flask Setup
#################################
app = Flask(__name__)

#################################
# Flask Routes endpoints
#################################

# Setting the home page,

@app.route("/")
def welcome():
    return (
        f"<h1>Welcome to the Hawaii Weather Analysis and API!</h1>"
        f"A Flask API for Climate Analysis.<br/><br/>"
        f"<h2>Here are the available routes:</h2>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/start_date<br/><br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

# This route queries and  returns precipitation data for the last 12 months in Json format.

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set
    date_last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query to retrieve the date and precipitation for the last 12 months
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                  filter(Measurement.date >= date_last_year).all()
    
    session.close()

    # Convert the query results to a dictionary all_precipitation using date as the key and prcp as the value
    all_precipitation = {date: prcp for date, prcp in precipitation_data}

    # Return the JSON representation of dictionary
    return jsonify(all_precipitation)

# This route queries and returns a list of weather stations in JSON format.

@app.route("/api/v1.0/stations")
def stations():
    #query all stations
    results = session.query(Station.station, Station.name).all()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
    
    session.close()

    # Return the JSON representation of dictionary
    return jsonify(all_stations)

# This route queries and returns temperature observations for the most active weather station for the last year in JSON format
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from the last data point in the database
    date_last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Finds the most active station
    active_station = session.query(Measurement.station).\
                            group_by(Measurement.station).\
                            order_by(func.count().desc()).first()

    # Get the station id of the most active station
    #This line is unpacking the value stored in the active_station tuple, 
    # expects a single value to be assigned to most_active_station_id. 
    # The use of the trailing comma makes it clear that you are unpacking a single item from the tuple
    
    #(most_active_station_id, ) = active_station
    
    #You can directly access the item in the tuple using indexing without unpacking
    most_active_station_id = active_station[0]

    # Query to retrieve the date and temperature for the most active station for the last one year.
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.station == most_active_station_id).\
                    filter(Measurement.date >= date_last_year).all()
    
    session.close()

    # flat list is one-dimensional list that contains only individual elements. do not have nested lists)
    #It flattens the tobs_data list of tuples into a flat list using NumPy's ravel function
    #converts it into a Python list
    all_temp = list(np.ravel(tobs_data))
    
    # Return the JSON representation
    return jsonify(all_temp)     

# This route takes a start date as a parameter and returns minimum, average, 
# and maximum temperature data from that date onwards in JSON format.

@app.route('/api/v1.0/<start>')
@app.route("/api/v1.0/<start>/<end>")
def start_date_stats(start, end=None):   #is responsible for querying temperature statistics from a database
  
                                          # based on specified date ranges using SQLAlchemy.
#check if 'end' date is provided or not.                                          
    if end != None:
        # query the database for temperature statistics(min, avg, max)
        temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        #If no 'end' date is provided, query for statistics from the 'start' date onwards 
    else:
        temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    session.close()

    # Convert the query results to a list.
    temp_list = []
    no_temp_data = False
    for tmin, tavg, tmax in temp_data:
        if tmin == None or tavg == None or tmax == None:
            no_temp_data = True
        temp_list.append(tmin)
        temp_list.append(tavg)
        temp_list.append(tmax)
        
    ## Check if temperature data was not found, and return an appropriate response. 
    if no_temp_data == True:
        return f"Temperature data not found. Try another date range."
    else:
        return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)

