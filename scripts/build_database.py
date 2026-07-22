from database import (
    count_duplicates,
    count_nulls,
    count_rows,
    get_connection,
    save_table,
    table_exists
)

from loaders import (
    load_airports,
    load_countries,
    load_frequencies,
    load_regions,
    load_runways
)

from logger import write_log, log_validation

REQUIRED_TABLES = [
    "airports",
    "runways",
    "frequencies",
    "countries",
    "regions"
]

REQUIRED_COLUMNS = {
    "airports": ["id", "ident", "type", "name"],
    "runways": ["id", "airport_ref"],
    "frequencies": ["id", "airport_ref"],
    "countries": ["id", "name"],
    "regions": ["id", "code", "name"]
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

def show_countries_without_code(connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, code, name, continent
        FROM countries
        WHERE code IS NULL
        """
    )

    rows = cursor.fetchall()

    print("\nCountries with missing code:")

    if rows:
        for row in rows:
            print(row)
    else:
        print("None")


def validate_required_columns(connection):

    for table, columns in REQUIRED_COLUMNS.items():

        for column in columns:

            nulls = count_nulls(
                table,
                column,
                connection
            )

            if nulls > 0:

                message = (
                    f"Table '{table}', column '{column}' "
                    f"contains {nulls} null value(s)."
                )

                write_log(
                    "ERROR",
                    message
                )

                raise Exception(message)

            message = (
                f"{table}.{column}: no null values."
            )

            print(
                f"✓ {table}.{column}: no null values"
            )

            write_log(
                "PASS",
                message
            )

def validate_country_codes(connection):

    nulls = count_nulls(
        "countries",
        "code",
        connection
    )

    if nulls > 0:

        message = (
            f"countries.code contains "
            f"{nulls} null value(s)."
        )

        print(f"WARNING: {message}")

        write_log(
            "WARNING",
            message
        )

    else:

        print(
            "✓ countries.code: no null values"
        )

        write_log(
            "PASS",
            "countries.code contains no null values."
        )


def main():

    print("Starting database build process...")

    write_log(
        "INFO",
        "Database build process started."
    )

    airports_clean = load_airports()
    runways_clean = load_runways()
    frequencies_clean = load_frequencies()
    countries_clean = load_countries()
    regions_clean = load_regions()

    connection = get_connection()

    try:

        save_table(
            airports_clean,
            "airports",
            connection
        )

        save_table(
            runways_clean,
            "runways",
            connection
        )

        save_table(
            frequencies_clean,
            "frequencies",
            connection
        )

        save_table(
            countries_clean,
            "countries",
            connection
        )

        save_table(
            regions_clean,
            "regions",
            connection
        )

        print("\nValidating tables...")
        validate_tables(connection)

        print("\nValidating duplicated IDs...")
        validate_duplicate_ids(connection)

        show_countries_without_code(connection)

        print("\nValidating required columns...")
        validate_required_columns(connection)

        validate_country_codes(connection)

        print(
            "\nAll validation checks passed successfully."
        )

    finally:

        connection.close()

        print("Database connection closed.")

    write_log(
        "INFO",
        "Database build process completed successfully."
    )
    print("Database build process completed.")


if __name__ == "__main__":
    main()