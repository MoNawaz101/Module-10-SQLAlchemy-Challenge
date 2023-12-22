# Import the dependencies.
import numpy as np
import datetime as dt
from datetime import datetime
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False      #stop JSon output being sorted alphabetically

#################################################
# Flask Routes
#################################################

# Part 2: 1. List Available Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Module 10 SQLAlchemy Challenge<br/><br/><br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"---Precipitation data<br/><br/>"
        f"/api/v1.0/stations<br/>"
        f"---Station codes and names<br/><br/>"
        f"/api/v1.0/tobs<br/>"
        f"---Temperature observations<br/><br/>"
        f"/api/v1.0/start<br/>"
        f"---Temperature summary from the start date till the end of the data"
        f"---start is the start date in the form YYYY-MM-DD <br/>"
        f"---The start date does not need double quotation marks <br/>"
        f"---Example call: /api/v1.0/2016-01-01  <br/><br/>"   
        f"/api/v1.0/start/end<br/>"
        f"---Temperature summary between two supplied dates"
        f"---Where start and end are the start and end dates in the form YYYY-MM-DD <br/>"
        f"---The dates do not need double quotation marks <br/>"
        f"---Example call: /api/v1.0/2016-01-01/2016-12-31  <br/><br/>"  
        )

# Part 2: 2. Precipitation Analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Find the date of the last data
    qry = session.query(func.max(measurement.date).label("last_date"))
    res = qry.one()
    last_date = res.last_date
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    # Subtract a year to get the start date for a year's worth of data
    start_date = last_date - relativedelta(days=366)

    """Return precipitation data for the last 12 months"""
    # Query all rows
    results = session.query(measurement.date,measurement.prcp).filter(measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        # The challenge instructions specify that the key should be the date which
        # I have done. Personally I think the hashed out lines produce data in a 
        # better format.
 #       precipitation_dict["date"] = date
 #       precipitation_dict["precipitation"] = prcp
        precipitation_dict = {date : prcp}
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


# Part 2: 3. List of Stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(station.station,station.name).all()

    session.close()  

    # Convert into a flat normal list as the instructions specified a list rather
    # than a dictionary
    all_stations = list(np.ravel(results))
 
    return jsonify(all_stations)


# Part 2: 4. Temperature Observations for the Most Active Station for the Previous Year 
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    qry = session.query(func.max(measurement.date).label("last_date"))
    res = qry.one()
    last_date = res.last_date
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    start_date = last_date - relativedelta(days=366)         #The data for the task requires 1Y and 1D
 
    qry = session.query(measurement.station,func.count(measurement.prcp)).\
        group_by(measurement.station).order_by(desc(func.count(measurement.prcp))).all()
    
    """Return temperature data for the last 12 months for the most active station"""
    results = session.query(measurement.date,measurement.tobs).\
            filter((measurement.station == qry[0][0]) & \
                   (measurement.date >= start_date)).all()

    session.close()

    # Create a dictionary from the row data and append to all_temp
    all_temp = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = tobs
        all_temp.append(temp_dict)

    return jsonify(all_temp)


# Part 2: 5. Temperature Summary Given a Start Date
@app.route("/api/v1.0/<start>")
def Temp_summary1(start):
    """Calculate the min, max and average temp from the start date supplied by the user to the end of the dataset."""

    upper_date = datetime.strptime("2017-08-23", '%Y-%m-%d')
    lower_date = datetime.strptime("2010-01-01", '%Y-%m-%d')

    try:
        # formatting the date using strptime() function
        start_date = datetime.strptime(start, '%Y-%m-%d')
        
        # Error check to see if the date requested doesn't exceed the range of dates available
        if (start_date > upper_date):
            return("Date is beyond the upper date range of 2017-08-23. No data exists beyond this date")
        elif (start_date < lower_date):
            return("Date is before the lower date range of 2010-01-01. No data exists before this date")
    except ValueError:
        # If the date validation goes wrong
        return("Incorrect date format, should be in form YYYY-MM-DD")
    
    session = Session(engine)
 
    TMAX = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date).all()
    TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date).all()
    TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()

    session.close()

    temp_data = { "Start date": start_date,"End date": upper_date+ relativedelta(days=1), "Max Temp": TMAX[0][0], "Min Temp": TMIN[0][0], "Avg Temp": round(TAVG[0][0],1)}

    return jsonify(temp_data)


# Part 2: 5. Temperature Summary Given a Start and an End Date
@app.route("/api/v1.0/<start>/<end>")
def Temp_summary2(start,end):
    """Calculate the min, max and average temp from the start date supplied by the user to the end of the dataset."""

    upper_date = datetime.strptime("2017-08-23", '%Y-%m-%d')
    lower_date = datetime.strptime("2010-01-01", '%Y-%m-%d')

    try:
        # formatting the date using strptime() function
        start_date = datetime.strptime(start, '%Y-%m-%d')
        # convert end_date to datetime and add 1 day because otherwise the datetime will be yyyy-mm-dd 00:00:00
        # when converted which will not include data from the last day.
        end_date = datetime.strptime(end, '%Y-%m-%d') + relativedelta(days=1)

        # Error check to see if the dates requested don't exceed the range of dates available and the dates are the correct way around.
        if (end_date > upper_date):
            return("Date is beyond the upper date range of 2017-08-23. No data exists beyond this date.")
        elif (start_date < lower_date):
            return("Date is before the lower date range of 2010-01-01. No data exists before this date.")
        elif (start_date > end_date):
            return("Start date is after the end date. Please put the other way around.")
    except ValueError:
        # If the date validation goes wrong
        return("Incorrect date format, should be in form YYYY-MM-DD")
    
    session = Session(engine)
 
    TMAX = session.query(func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    TMIN = session.query(func.min(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    TAVG = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()

    temp_data = { "Start date": start_date,"End date": end_date, "Max Temp": TMAX[0][0], "Min Temp": TMIN[0][0], "Avg Temp": round(TAVG[0][0],1)}

    return jsonify(temp_data)

 
if __name__ == '__main__':
    app.run(debug=True)


