# Smart Parking Data Engineering Pipeline

This project is a beginner-friendly data engineering pipeline that simulates parking lot activity, transforms raw parking records into analytics-ready data, loads the result into MongoDB, and visualizes it with a simple dashboard.

## Overview

This project demonstrates a small end-to-end data engineering workflow:

- Generate synthetic parking data
- Store raw data as CSV
- Transform and enrich the dataset
- Load processed data into MongoDB
- View summary metrics in a Streamlit dashboard

## Tech Stack

- Python
- Pandas
- Faker
- MongoDB
- PyMongo
- Streamlit

## Project Stages

1. Setup and structure
2. Data generation
3. Data transformation
4. Load into MongoDB
5. Full pipeline automation
6. Upgrade path: scheduler and dashboard

## Project Structure

```text
parking-data-pipeline/
|-- data/
|   |-- parking_data.csv
|   |-- parking_data_transformed.csv
|-- dashboard/
|   |-- app.py
|-- scripts/
|   |-- generate_data.py
|   |-- transform_data.py
|   |-- load_to_mongodb.py
|   |-- scheduler.py
|-- .env.example
|-- .gitignore
|-- main.py
|-- README.md
|-- requirements.txt
```

## Data Flow

- `scripts/generate_data.py` creates raw parking event data as CSV.
- `scripts/transform_data.py` cleans and enriches the raw dataset.
- `scripts/load_to_mongodb.py` loads transformed data into MongoDB.
- `main.py` runs the full pipeline end to end.

```text
Generate raw parking events
        ->
data/parking_data.csv
        ->
data/parking_data_transformed.csv
        ->
MongoDB collection
        ->
Streamlit dashboard
```

## Setup

```bash
pip install -r requirements.txt
```

Create a local `.env` file:

```env
MONGODB_URI=mongodb://localhost:27017/
```

## Run Each Stage

Generate raw data:

```bash
python scripts/generate_data.py
```

Transform the dataset:

```bash
python scripts/transform_data.py
```

Load into MongoDB:

```bash
python scripts/load_to_mongodb.py
```

Run the full pipeline:

```bash
python main.py --records 100
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Engineered Fields

The transformation stage adds:

- `duration_minutes`
- `duration_hours`
- `parking_fee`
- `entry_date`
- `entry_hour`
- `is_peak_hour`
- `parking_status`



