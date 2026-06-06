# Earthquake ETL Pipeline and Analytics Dashboard

## Project Overview

This project demonstrates an end-to-end Data Engineering and Analytics workflow using real-time earthquake data from the United States Geological Survey (USGS) API.

The project extracts earthquake event data, performs transformation and validation, loads the cleaned data into a PostgreSQL database hosted on Supabase, and provides an interactive analytics dashboard built with Dash.

---

## Technologies Used

* Python
* Pandas
* Requests
* SQLAlchemy
* PostgreSQL
* Supabase
* Dash
* Plotly
* GitHub

---

## ETL Pipeline

### Extract

Data is collected from the USGS Earthquake API.

Information extracted includes:

* Earthquake ID
* Magnitude
* Location
* Latitude
* Longitude
* Depth
* Event Time
* Earthquake Type

### Transform

Data transformation includes:

* Converting timestamps to datetime format
* Creating magnitude categories
* Removing duplicate earthquake IDs
* Removing records with missing magnitude values
* Preparing analytics-ready datasets

### Validate

Validation checks include:

* Null value checks
* Duplicate record checks
* Magnitude range validation

### Load

Validated records are loaded into a PostgreSQL database hosted on Supabase.

The pipeline supports incremental loading by preventing duplicate earthquake records from being inserted.

---

## Dashboard Features

The Dash application provides interactive analytics for earthquake events.

### KPI Card

* Total Earthquakes

### Visualizations

1. Earthquakes by Magnitude Category

   * Bar Chart

2. Earthquakes Over Time

   * Time Series Line Chart

### Interactive Features

* Magnitude Category Dropdown Filter
* Dynamic KPI Updates
* Dynamic Chart Updates

---

## Business Insights

The dashboard enables users to:

* Monitor earthquake activity trends over time
* Compare earthquake magnitude categories
* Identify patterns in earthquake frequency
* Analyze the distribution of seismic events

---

## Project Structure

```text
earthquake-etl-pipeline/
│
├── earthquake_etl.py
├── dashboard.py
├── requirements.txt
├── README.md
│
└── output/
    └── earthquake_analytics.csv
```

---

## How to Run the ETL Pipeline

Activate the virtual environment:

```bash
.venv\Scripts\activate
```

Run the ETL pipeline:

```bash
python earthquake_etl.py
```

---

## How to Run the Dashboard

Start the Dash application:

```bash
uv run dashboard.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:8050
```

---

## Database

Database Platform:

* PostgreSQL
* Supabase Cloud

The ETL pipeline loads validated earthquake data directly into the PostgreSQL database.

---

## Screenshots

### ETL Pipeline Execution

Insert screenshot here.

### Supabase Database Table

Insert screenshot here.

### Dashboard Overview

Insert screenshot here.

### Dashboard with Interactive Filter

Insert screenshot here.

---

## GitHub Repository

Repository Link:

https://github.com/Sindhujaa123/earthquake-etl-pipeline

---

## Author

Sindhujaa

Data Engineering Pipeline and Analytics Dashboard Project
