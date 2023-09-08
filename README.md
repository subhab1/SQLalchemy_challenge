# SQLalchemy_challenge
## Background:
This repository is designed to make a climate analysis on Hawaii, and discover hidden patterns, unseen trends before planning a vacation. We are using Sqlalchemy to establish a connection to the Hawaii.sqlite database through python application. Sqlalchemy is a python library that makes it easier to work with databases in their application by making it more manageable. Think of it as a bridge between your python code and a database like PostgreSQL, MYSQL, and SQLite.
### Step 1
* This project used a Python and SQLAlchemy to make climate analysis, and data exploration of the climate database. All of the analysis was completed by using SQLAlchemy ORM queries, Pandas, and Matplotlib.
 SQLAlchemy engin created create_engine to connect to the sqlite database. engine = create_engine("sqlite:///Resources/hawaii.sqlite") inspector = inspect(engine)`
To reflect the tables into classes, and save a reference to those classes called Station and Measurement an SQLAlchemy automap_base() is used.

### Step 2 - Climate App
After the initial analysis was completed, a Flask API designed based on the queries already developed.

The following routes are created by using Flask.
* Routes "/"
Home page.

* List all routes that are available.

    /api/v1.0/precipitation

* Convert the query results to a dictionary using date as the key and prcp as the value.

* Return the JSON representation of your dictionary.

    /api/v1.0/stations

* Return a JSON list of stations from the dataset.
    /api/v1.0/tobs

* Query the dates and temperature observations of the most active station for the last year of data.

* Return a JSON list of temperature observations (TOBS) for the previous year.

    /api/v1.0/<start> and /api/v1.0/<start>/<end>

* Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

* When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

* When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


