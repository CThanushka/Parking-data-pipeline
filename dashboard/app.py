import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

st.set_page_config(page_title="Smart Parking Dashboard", layout="wide")

mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
client = MongoClient(mongodb_uri)
collection = client["smart_parking"]["parking_events"]

records = list(collection.find({}, {"_id": 0}))

st.title("Smart Parking Dashboard")
st.caption("View of parking activity, usage, and revenue.")

if not records:
    st.warning("No parking data found in MongoDB yet. Run `python main.py --records 50` first.")
else:
    df = pd.DataFrame(records)
    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])

    total_events = len(df)
    total_revenue = float(df["parking_fee"].sum())
    avg_duration = float(df["duration_hours"].mean())

    col1, col2, col3 = st.columns(3)
    col1.metric("Parking Events", total_events)
    col2.metric("Total Revenue", f"${total_revenue:.2f}")
    col3.metric("Avg Duration (hrs)", f"{avg_duration:.2f}")

    st.subheader("Revenue by Vehicle Type")
    revenue_by_vehicle = (
        df.groupby("vehicle_type", as_index=False)["parking_fee"].sum().sort_values("parking_fee", ascending=False)
    )
    st.bar_chart(revenue_by_vehicle.set_index("vehicle_type"))

    st.subheader("Entries by Zone")
    zone_counts = df.groupby("zone", as_index=False)["event_id"].count().rename(columns={"event_id": "events"})
    st.bar_chart(zone_counts.set_index("zone"))

    st.subheader("Recent Parking Events")
    st.dataframe(
        df.sort_values("entry_time", ascending=False)[
            [
                "event_id",
                "vehicle_no",
                "vehicle_type",
                "zone",
                "slot",
                "entry_time",
                "exit_time",
                "duration_hours",
                "parking_fee",
            ]
        ],
        width="stretch",
    )

client.close()
