from .database import (
    count_duplicates,
    count_nulls,
    get_countries_without_code,
    table_exists
)

from .logger import log_validation


REQUIRED_TABLES = [
    "airports",
    "runways",
    "frequencies",
    "countries",
    "regions",
    "airport_weather"
]

REQUIRED_COLUMNS = {
    "airports": ["id", "ident", "type", "name"],
    "runways": ["id", "airport_ref"],
    "frequencies": ["id", "airport_ref"],
    "countries": ["id", "name"],
    "regions": ["id", "code", "name"],
    "airport_weather": [
        "airport_id",
        "airport_ident",
        "airport_name",
        "weather_time",
        "temperature_c",
        "weather_code",
        "wind_speed_kmh",
        "monitoring_priority"
    ]
}

TABLES_WITH_UNIQUE_ID = [
    "airports",
    "runways",
    "frequencies",
    "countries",
    "regions"
]


def validate_tables(connection):

    for table in REQUIRED_TABLES:

        if not table_exists(
            table,
            connection
        ):
            log_validation(
                "ERROR",
                f"Required table '{table}' does not exist."
            )

        log_validation(
            "PASS",
            f"Table '{table}' exists."
        )


def validate_duplicate_ids(connection):

    for table in TABLES_WITH_UNIQUE_ID:

        duplicates = count_duplicates(
            table,
            "id",
            connection
        )

        if duplicates > 0:
            log_validation(
                "ERROR",
                (
                    f"Table '{table}' contains "
                    f"{duplicates} duplicated ID value(s)."
                )
            )

        log_validation(
            "PASS",
            f"{table}: no duplicated IDs."
        )


def validate_required_columns(connection):

    for table, columns in REQUIRED_COLUMNS.items():

        for column in columns:

            null_count = count_nulls(
                table,
                column,
                connection
            )

            if null_count > 0:
                log_validation(
                    "ERROR",
                    (
                        f"Table '{table}', column '{column}' "
                        f"contains {null_count} null values."
                    )
                )

            log_validation(
                "PASS",
                (
                    f"Table '{table}', column '{column}' "
                    "contains no null values."
                )
            )


def validate_country_codes(connection):

    null_count = count_nulls(
        "countries",
        "code",
        connection
    )

    if null_count > 0:
        log_validation(
            "WARNING",
            (
                "Table 'countries', column 'code' "
                f"contains {null_count} null values."
            )
        )
    else:
        log_validation(
            "PASS",
            (
                "Table 'countries', column 'code' "
                "contains no null values."
            )
        )


def show_countries_without_code(connection):

    rows = get_countries_without_code(connection)

    print("Countries with missing code:")

    if rows:
        for row in rows:
            print(row)
    else:
        print("None")