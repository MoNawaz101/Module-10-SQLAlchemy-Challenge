# Module-10-SQLAlchemy-Challenge

## Task Instructions  
Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. The following sections outline the steps that you need to take to accomplish this task. The challenge is in two parts:

### Part 1: Analyze and Explore the Climate Data
Use Python and SQLAlchemy to do a basic climate analysis and data exploration of a climate database. More specifically, using SQLAlchemy ORM queries, Pandas, and Matplotlib.

### Part 2: Design a Climate App
A Flask API is designed based on the queries that were developed in Part 1.

## Contents  
- [Directory structure](#Directory-structure)
- [CSV files](#CSV-files)
- [Sqlite Database](#Sqlite-Database)
- [Analysis files](#Analysis-files)
- [Python file](#Python-files)

## Directory structure 
The root directory contains:  
- [SurfsUp](/SurfsUp) - This folder contains the Jupyter notebook and Python analysis files as well as Resources folder.  
- [SurfsUP/Resources](/SurfsUp/Resources/)  - This folder contains the original CSV files and an SQLlite database.

## CSV files 
These are the original CSV files provided for the challenge in the [SurfsUP/Resources/](/SurfsUp/Resources/) folder.
- hawaii_stations.csv  -  Data on the weather stations in Hawaii that collected the weather data.
- hawaii_measurements.csv - Precipitation and temperature data for all the stations collected per day.

## Sqlite Database
In the folder [Resources/](/SurfsUp/Resources/).
Contains all the CSV data.

## Analysis files
[climate_starter.ipynb](/SurfsUp/climate_starter.ipynb)  
This file is used to do the Part 1 analysis.
- Precipitation Analysis. Produces a graph of precipitation from all stations for the last year.
- Station Analysis. A temperature summary is produced for the most active station on the island. A temperature graph is produced.

[app.py](/SurfsUp/app.py)   
This file is used to do the Part 2 analysis.  
A FLask API is designed based on the tasks completed in Part 1.
The API has the following routes:
- /api/v1.0/precipitation.
- /api/v1.0/stations
- /api/v1.0/stations
-	/api/v1.0/tobs
- /api/v1.0/<start>
- /api/v1.0/<start> 


