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
