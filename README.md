# Earthquake ETL Pipeline

## Project Overview

This project implements a Python ETL (Extract, Transform, Load) pipeline using earthquake data from the USGS Earthquake API. The pipeline extracts raw earthquake records, performs data cleaning and transformation, validates data quality, exports an analytics-ready dataset, and loads the processed records into a PostgreSQL database hosted on Supabase.

## Data Source

USGS Earthquake API

https://earthquake.usgs.gov/

## Features

* API data extraction
* Data cleaning and transformation
* Missing value handling
* Duplicate detection
* Data validation checks
* Derived metric creation (magnitude category)
* Analytics-ready CSV export
* Incremental loading strategy
* PostgreSQL database loading
* Logging and error handling

## Technologies Used

* Python
* Pandas
* Requests
* SQLAlchemy
* PostgreSQL
* Supabase

## Output

The pipeline generates:

* earthquake_analytics.csv
* Populated earthquake_events database table

## Execution

Run the pipeline using:

python earthquake_etl.py

## Incremental Loading Strategy

The pipeline prevents duplicate records by checking existing earthquake_id values in the database and loading only new records.

## Author

Sindhujaa
