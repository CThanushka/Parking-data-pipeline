import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_OUTPUT_PATH = DATA_DIR / "parking_data.csv"

VEHICLE_TYPES = {
    "car": 2.5,
    "motorbike": 1.0,
    "van": 3.5,
    "suv": 3.0,
}


def generate_parking_data(n: int = 50, output_path: Path = RAW_OUTPUT_PATH) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    records = []

    for _ in range(n):
        vehicle_type = random.choice(list(VEHICLE_TYPES.keys()))
        zone = random.choice(["A", "B", "C"])
        slot_number = random.randint(1, 50)
        entry_time = datetime.now() - timedelta(
            hours=random.randint(1, 24),
            minutes=random.randint(0, 59),
        )
        parking_duration = timedelta(minutes=random.randint(30, 360))
        exit_time = entry_time + parking_duration

        records.append(
            {
                "event_id": str(uuid.uuid4()),
                "vehicle_no": fake.license_plate(),
                "vehicle_type": vehicle_type,
                "zone": zone,
                "slot": f"{zone}{slot_number}",
                "entry_time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                "exit_time": exit_time.strftime("%Y-%m-%d %H:%M:%S"),
                "payment_method": random.choice(["cash", "card", "app"]),
                "parking_rate_per_hour": VEHICLE_TYPES[vehicle_type],
            }
        )

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    output_file = generate_parking_data()
    print(f"Parking data generated at {output_file}")
