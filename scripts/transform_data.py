from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "parking_data.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "parking_data_transformed.csv"


def transform_parking_data(
    input_path: Path = RAW_DATA_PATH,
    output_path: Path = PROCESSED_DATA_PATH,
) -> Path:
    df = pd.read_csv(input_path)

    df["entry_time"] = pd.to_datetime(df["entry_time"])
    df["exit_time"] = pd.to_datetime(df["exit_time"])

    invalid_rows = df["exit_time"] < df["entry_time"]
    if invalid_rows.any():
        raise ValueError("Found records where exit_time is earlier than entry_time.")

    duration = df["exit_time"] - df["entry_time"]
    df["duration_minutes"] = (duration.dt.total_seconds() / 60).round(2)
    df["duration_hours"] = (duration.dt.total_seconds() / 3600).round(2)
    df["parking_fee"] = (df["duration_hours"] * df["parking_rate_per_hour"]).round(2)
    df["entry_date"] = df["entry_time"].dt.date.astype(str)
    df["entry_hour"] = df["entry_time"].dt.hour
    df["is_peak_hour"] = df["entry_hour"].between(8, 10) | df["entry_hour"].between(17, 19)
    df["parking_status"] = "completed"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    output_file = transform_parking_data()
    print(f"Transformed data saved to {output_file}")
