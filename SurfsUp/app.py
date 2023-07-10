# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

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
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
       f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipatation():
    #Query to retrieve the last 12 months of precipitation data
    Year_Prcp_data = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date > '2016-08-22').order_by(Measurement.date).all()

    #Convert query results to a dictionary
    Prcp_Data = []
    for date, prcp in Year_Prcp_data:
        Prcp_Dict = {}
        Prcp_Dict["date"] = date
        Prcp_Dict["prcp"] = prcp
        Prcp_Data.append(Prcp_Dict)
    
    return jsonify(Prcp_Data)

@app.route("/api/v1.0/stations")
def stations():
    #Query to retrieve list of stations 
    stations = session.query(Station.station, Station.name).all()

    #Convert query results to a dictionary
    Stations_info = []
    for station, name in stations:
        Stations_Dict = {}
        Stations_Dict["station"] = station
        Stations_Dict["name"] = name
        Stations_info.append(Stations_Dict)
    
    return jsonify (Stations_info)

@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most-active station for the previous year of data.
    Year_station_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-17')\
        .filter(Measurement.station == "USC00519281")\
        .order_by(Measurement.date).all()
    
    #Convert query results to a dictionary
    tobs_data = []
    for date, tobs in Year_station_data:
        Tobs_Dict = {}
        Tobs_Dict["date"] = date
        Tobs_Dict["tobs"] = tobs
        tobs_data.append(Tobs_Dict)
    
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    #Query min, max, avg tobs for entered start date
    start_date_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    #Return a JSON list of the minimum temperature, the average temperature, and the max for specified date
    start_date_data =[]
    for min, avg, max in start_date_results:
        Start_date_dict = {}
        Start_date_dict["min"] = min
        Start_date_dict["average"] = avg
        Start_date_dict["max"] = max
        start_date_data.append(Start_date_dict)
    
    return jsonify(start_date_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    #Query min, max, avg tobs for entered start and end date
    start_end_date_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
#Return a JSON list of the minimum temperature, the average temperature, and the max for specified dates
    start_end_date_data =[]
    for min, avg, max in start_end_date_results:
        Start_end_date_dict = {}
        Start_end_date_dict["min"] = min
        Start_end_date_dict["average"] = avg
        Start_end_date_dict["max"] = max
        start_end_date_data.append(Start_end_date_dict)
    
    return jsonify(start_end_date_data)

if __name__ == "__main__":
    app.run(debug=True)