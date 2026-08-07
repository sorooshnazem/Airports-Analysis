from .database import (
    get_connection,
    save_table
)

from .loaders import (
    load_countries,
    load_frequencies,
    load_regions,
    load_runways,
    load_airports
)

from .validators import (
    validate_country_codes,
    validate_duplicate_ids,
    validate_required_columns,
    validate_tables,
    show_countries_without_code
)

from .api_client import get_current_weather
from .database import get_airport_by_ident
from .transforms import transform_current_weather

import pandas as pd


def build_airports_table():

    airports = load_airports()

    connection = get_connection()

    try:
        save_table(
            airports,
            "airports",
            connection
        )

    finally:
        connection.close()

def build_runways_table():

    runways = load_runways()

    connection = get_connection()

    try:
        save_table(
            runways,
            "runways",
            connection
        )

    finally:
        connection.close()


def build_frequencies_table():

    frequencies = load_frequencies()

    connection = get_connection()

    try:
        save_table(
            frequencies,
            "frequencies",
            connection
        )

    finally:
        connection.close()


def build_countries_table():

    countries = load_countries()

    connection = get_connection()

    try:
        save_table(
            countries,
            "countries",
            connection
        )

    finally:
        connection.close()


def build_regions_table():

    regions = load_regions()

    connection = get_connection()

    try:
        save_table(
            regions,
            "regions",
            connection
        )

    finally:
        connection.close()


def validate_database():

    connection = get_connection()

    try:

        validate_tables(connection)

        validate_duplicate_ids(connection)

        show_countries_without_code(connection)

        validate_required_columns(connection)

        validate_country_codes(connection)

    finally:

        connection.close()


def get_airport_weather(airport_ident):

    connection = get_connection()

    try:

        airport = get_airport_by_ident(
            airport_ident,
            connection
        )

        if airport is None:
            raise ValueError(
                f"Airport '{airport_ident}' was not found."
            )

        airport_id = airport[0]
        airport_ident = airport[1]
        airport_name = airport[2]
        latitude = airport[3]
        longitude = airport[4]

        weather_response = get_current_weather(
            latitude=latitude,
            longitude=longitude
        )

        return transform_current_weather(
            weather_response=weather_response,
            airport_id=airport_id,
            airport_ident=airport_ident,
            airport_name=airport_name
        )

    finally:
        connection.close()


def build_airport_weather_table(airport_ident):

    weather = get_airport_weather(
        airport_ident
    )

    weather_dataframe = pd.DataFrame(
        [weather]
    )

    connection = get_connection()

    try:
        save_table(
            weather_dataframe,
            "airport_weather",
            connection
        )

    finally:
        connection.close()
