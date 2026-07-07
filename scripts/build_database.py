import sqlite3
import pandas as pd
from database import get_connection, save_table, count_rows
from loaders import (
    load_airports,
    load_runways,
    load_frequencies,
    load_countries,
    load_regions
)

DATABASE_PATH = "database/airports.db"
AIRPORTS_CSV_PATH = "data/airports.csv"
RUNWAYS_CSV_PATH = "data/runways.csv"
FREQUENCIES_CSV_PATH = "data/airport-frequencies.csv"

def main():

    print("Starting database build process...")

    airports_clean = load_airports()

    runways_clean = load_runways()

    frequencies_clean = load_frequencies()

    countries_clean = load_countries()

    regions_clean = load_regions()

    connection = get_connection()

    save_table(airports_clean, "airports", connection)
    save_table(runways_clean, "runways", connection)
    save_table(frequencies_clean, "frequencies", connection)
    save_table(countries_clean, "countries", connection)
    save_table(regions_clean, "regions", connection)

    print(f"Rows in airports table: {count_rows('airports', connection)}")
    print(f"Rows in runways table: {count_rows('runways', connection)}")
    print(f"Rows in frequencies table: {count_rows('frequencies', connection)}")
    print(f"Rows in countries table: {count_rows('countries', connection)}")
    print(f"Rows in regions table: {count_rows('regions', connection)}")

    connection.close()

    print("Database build process completed.")


if __name__ == "__main__":
    main()