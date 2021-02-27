# SQLAlchemy - Surfs Up!

## Background
This project involves climate analysis on Honolulu, Hawaii and the surrounding area.

## Step 1 - Climate Analysis and Exploration

Python and SQLAlchemy were used to do basic climate analysis and data exploration of the climate database. Each of the following analyses were completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* A hypothetical trip date of 9/8-9/15 is selected.

* SQLAlchemy is used to `create_engine` to connect to the sqlite database.

* SQLAlchemy `automap_base()` is used to reflect the tables into classes.  References to those classes called `Station` and `Measurement` are saved.

### Precipitation Analysis

* A query retrieves the last 12 months of precipitation data using only the `date` and `prcp` values.

* The query results are loaded into a Pandas DataFrame and the index is set to the date column. The DataFrame is sorted by `date`.

* The results are plotted using the DataFrame `plot` method.

* Pandas summary statistics are derived for the precipitation data.

### Station Analysis

* A query calculates the total number of stations.

* Another query finds the most active station and lists the stations and observation counts in descending order.

* A third query retrieves the last 12 months of temperature observation data (TOBS), filters by the station with the highest number of observations. The results are plotted in a histogram with 12 bins.

- - -

## Step 2 - Climate App

A Flask API was designed based on the queries that were developed.

### Routes

* `/`

  * Home page - lists all routes that are available.

* `/api/v1.0/precipitation`

  * Converts the query results to a dictionary using `date` as the key and `prcp` as the value. This return the JSON representation of the dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Queries the dates and temperature observations of the most active station for the last year of data and returns a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` 

  * Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date.
  * When given the start only, calculates `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  
`/api/v1.0/<start>/<end>`
  * Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
  * When given the start and the end date, calculates the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.


## Other Analyses

### Temperature Analysis

* Uses the `calc_temps` function (which accepts a start and end date in the format `%Y-%m-%d`)to calculate the min, avg, and max temperatures for a hypothetical trip using the matching dates from the previous year.

* Plots the min, avg, and max temperature from the previous query as a bar chart.
  * Uses the average temperature as the bar height.
  * Uses the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

### Daily Rainfall Average
This portion of the code:

* Calculates the rainfall per weather station using the previous year's matching dates.

* Calculates the daily normals. Normals are the averages for the min, avg, and max temperatures.

* The function called `daily_normals` will calculate the daily normals for a specific date, with date in the format `%m-%d`. The function uses all historic TOBS that match that date string.

* Creates a list of dates for your trip in the format `%m-%d`. Uses the `daily_normals` function to calculate the normals for each date string and appends the results to a list.

* Loads the list of daily normals into a Pandas DataFrame and set the index equal to the date.

* Uses Pandas to plot an area plot (`stacked=False`) for the daily normals.



