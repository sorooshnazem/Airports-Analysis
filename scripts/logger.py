from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOG_DIRECTORY = PROJECT_ROOT / "logs"
LOG_DIRECTORY.mkdir(exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "pipeline.log"


def write_log(level, message):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"[{timestamp}] [{level}] {message}\n"
        )

def log_validation(level, message):

    if level == "PASS":
        print(f"✓ {message}")

    elif level == "WARNING":
        print(f"WARNING: {message}")

    elif level == "ERROR":
        print(f"ERROR: {message}")

    write_log(
        level,
        message
    )

    if level == "ERROR":
        raise Exception(message)