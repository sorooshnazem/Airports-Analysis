from .database import (
    get_connection,
    save_table
)

from .loaders import (
    load_airports,
    load_countries,
    load_frequencies,
    load_regions,
    load_runways
)

from .logger import write_log

from .validators import (
    show_countries_without_code,
    validate_country_codes,
    validate_duplicate_ids,
    validate_required_columns,
    validate_tables
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

        print("\nChecking countries without code...")
        show_countries_without_code(connection)

        print("\nValidating required columns...")
        validate_required_columns(connection)

        print("\nValidating country codes...")
        validate_country_codes(connection)

        print("\nValidation completed successfully.")

        write_log(
            "PASS",
            "Validation completed successfully."
        )

    finally:

        connection.close()

        print("Database connection closed.")

        write_log(
            "INFO",
            "Database connection closed."
        )

    write_log(
        "INFO",
        "Database build process completed successfully."
    )

    print("Database build process completed.")


if __name__ == "__main__":
    main()