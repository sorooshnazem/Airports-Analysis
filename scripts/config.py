from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIRECTORY = PROJECT_ROOT / "data"
DATABASE_DIRECTORY = PROJECT_ROOT / "database"
LOG_DIRECTORY = PROJECT_ROOT / "logs"

DATABASE_FILE = DATABASE_DIRECTORY / "airports.db"
LOG_FILE = LOG_DIRECTORY / "pipeline.log"

AIRPORTS_CSV = DATA_DIRECTORY / "airports.csv"
RUNWAYS_CSV = DATA_DIRECTORY / "runways.csv"
FREQUENCIES_CSV = DATA_DIRECTORY / "airport-frequencies.csv"
COUNTRIES_CSV = DATA_DIRECTORY / "countries.csv"
REGIONS_CSV = DATA_DIRECTORY / "regions.csv"


DATABASE_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)