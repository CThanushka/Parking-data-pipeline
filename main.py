import argparse

from scripts.generate_data import generate_parking_data
from scripts.load_to_mongodb import load_to_mongodb
from scripts.transform_data import transform_parking_data


def run_pipeline(records: int) -> None:
    raw_path = generate_parking_data(n=records)
    transformed_path = transform_parking_data(input_path=raw_path)
    loaded_count = load_to_mongodb(input_path=transformed_path)

    print("Smart parking pipeline completed successfully.")
    print(f"Raw data: {raw_path}")
    print(f"Processed data: {transformed_path}")
    print(f"MongoDB records loaded: {loaded_count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart Parking Data Engineering Pipeline")
    parser.add_argument(
        "--records",
        type=int,
        default=50,
        help="Number of parking events to generate for the pipeline run.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(records=args.records)
