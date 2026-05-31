import requests
import pandas as pd
import logging
DATABASE_URL = "postgresql://postgres:Sindhujaa123@db.ehwzudsydyvhzxypaups.supabase.co:5432/postgres"
import os
from sqlalchemy import create_engine

# ----------------------------
# Logging Configuration
# ----------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Starting Earthquake ETL Pipeline")

# ----------------------------
# Extract Earthquake Data
# ----------------------------

def extract_earthquake_data():

    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            logging.info("API request successful")
            return response.json()

        else:
            logging.error(f"API request failed: {response.status_code}")
            return None

    except Exception as e:
        logging.error(f"Error during extraction: {e}")
        return None


raw_data = extract_earthquake_data()

if raw_data:
    print("Data extracted successfully")
else:
    print("Data extraction failed")

    # ----------------------------
# Transform Data
# ----------------------------

def transform_data(raw_data):

    records = []

    for feature in raw_data["features"]:

        properties = feature["properties"]
        geometry = feature["geometry"]

        magnitude = properties.get("mag")

        # Derived Metric
        if magnitude is None:
            magnitude_category = "Unknown"
        elif magnitude < 4:
            magnitude_category = "Minor"
        elif magnitude < 6:
            magnitude_category = "Moderate"
        else:
            magnitude_category = "Major"

        records.append({
            "earthquake_id": feature["id"],
            "magnitude": magnitude,
            "place": properties.get("place"),
            "latitude": geometry["coordinates"][1],
            "longitude": geometry["coordinates"][0],
            "depth": geometry["coordinates"][2],
            "event_time": pd.to_datetime(
                properties.get("time"),
                unit="ms"
            ),
            "earthquake_type": properties.get("type"),
            "magnitude_category": magnitude_category
        })

    df = pd.DataFrame(records)

# Remove rows with missing magnitude
    df = df.dropna(subset=["magnitude"])

# Remove duplicate earthquake IDs
    df = df.drop_duplicates(subset=["earthquake_id"])

    logging.info(f"Records extracted: {len(df)}")

    return df


df = transform_data(raw_data)

print(df.head())
# ----------------------------
# Data Quality Checks
# ----------------------------

def validate_data(df):

    logging.info("Starting data validation")

    # Null Value Check
    null_count = df.isnull().sum().sum()

    if null_count == 0:
        logging.info("Null check passed")
    else:
        logging.warning(f"Found {null_count} null values")

    # Duplicate Check
    duplicate_count = df["earthquake_id"].duplicated().sum()

    if duplicate_count == 0:
        logging.info("Duplicate check passed")
    else:
        logging.warning(f"Found {duplicate_count} duplicate IDs")

    # Magnitude Range Check
    invalid_magnitude = df[
        (df["magnitude"] < -2) |
        (df["magnitude"] > 10)
    ]

    if len(invalid_magnitude) == 0:
        logging.info("Magnitude range validation passed")
    else:
        logging.warning(
            f"Found {len(invalid_magnitude)} invalid magnitude values"
        )

    # Row Count Check
    logging.info(f"Total records: {len(df)}")

    return df


df = validate_data(df)
# ----------------------------
# Export Analytics Dataset
# ----------------------------

os.makedirs("output", exist_ok=True)

csv_path = "output/earthquake_analytics.csv"

df.to_csv(csv_path, index=False)

logging.info(f"Analytics dataset saved to {csv_path}")

# ----------------------------
# Database Loading
# ----------------------------

def load_to_database(df):

    try:

        engine = create_engine(DATABASE_URL)

        # Read existing IDs from database
        try:
            existing_df = pd.read_sql(
                "SELECT earthquake_id FROM earthquake_events",
                engine
            )
# Incremental Loading Strategy:
# Load only records whose earthquake_id
# does not already exist in the database.
# This prevents duplicate records when
# the ETL pipeline is run multiple times.
            existing_ids = set(existing_df["earthquake_id"])

        except Exception:
            existing_ids = set()

        # Incremental Loading
        new_records = df[
            ~df["earthquake_id"].isin(existing_ids)
        ]

        logging.info(
            f"New records to load: {len(new_records)}"
        )

        if len(new_records) > 0:

            new_records.to_sql(
                "earthquake_events",
                engine,
                if_exists="append",
                index=False
            )

            logging.info(
                f"{len(new_records)} records loaded successfully"
            )

        else:
            logging.info("No new records found")

    except Exception as e:

        logging.error(
            f"Database load failed: {e}"
        )


load_to_database(df)