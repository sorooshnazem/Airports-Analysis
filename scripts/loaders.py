import pandas as pd

from config import (
    AIRPORTS_CSV,
    RUNWAYS_CSV,
    FREQUENCIES_CSV,
    COUNTRIES_CSV,
    REGIONS_CSV
)
from transforms import select_columns, fill_missing_text


def load_csv(file_path, selected_columns):

    dataframe = pd.read_csv(file_path)

    print(f"Loaded {len(dataframe)} rows from {file_path}.")

    dataframe = select_columns(
        dataframe,
        selected_columns
    )

    print(f"Selected {len(dataframe.columns)} columns.")

    return dataframe


def load_airports():

    airports = load_csv(
        AIRPORTS_CSV,
        [
            "id",
            "ident",
            "type",
            "name",
            "latitude_deg",
            "longitude_deg",
            "elevation_ft",
            "iso_country",
            "iso_region",
            "municipality",
            "scheduled_service"
        ]
    )

    airports = fill_missing_text(
        airports,
        ["municipality"],
        "Unknown"
    )

    return airports


def load_runways():

    return load_csv(
        RUNWAYS_CSV,
        [
            "id",
            "airport_ref",
            "airport_ident",
            "length_ft",
            "width_ft",
            "surface",
            "lighted",
            "closed"
        ]
    )


def load_frequencies():

    return load_csv(
        FREQUENCIES_CSV,
        [
            "id",
            "airport_ref",
            "airport_ident",
            "type",
            "description",
            "frequency_mhz"
        ]
    )


def load_countries():

    return load_csv(
        COUNTRIES_CSV,
        [
            "id",
            "code",
            "name",
            "continent"
        ]
    )


def load_regions():

    return load_csv(
        REGIONS_CSV,
        [
            "id",
            "code",
            "local_code",
            "name",
            "continent",
            "iso_country"
        ]
    )