import sqlite3

from scripts.database import (
    count_rows,
    table_exists
)

def test_create_table_and_count_rows():

    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE airports (
            id INTEGER,
            name TEXT
        )
        """
    )

    connection.execute(
        """
        INSERT INTO airports
        VALUES
            (1, 'Airport A'),
            (2, 'Airport B')
        """
    )

    connection.commit()

    assert table_exists(
        "airports",
        connection
    )

    assert count_rows(
        "airports",
        connection
    ) == 2

    connection.close()
