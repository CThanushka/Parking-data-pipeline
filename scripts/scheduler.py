import time
import sys
from pathlib import Path

import schedule

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from main import run_pipeline


def scheduled_job() -> None:
    print("Running scheduled smart parking pipeline...")
    run_pipeline(records=25)


if __name__ == "__main__":
    schedule.every(1).minutes.do(scheduled_job)
    print("Scheduler started. Pipeline will run every 1 minute.")

    while True:
        schedule.run_pending()
        time.sleep(1)
