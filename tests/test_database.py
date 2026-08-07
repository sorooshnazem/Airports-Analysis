import sqlite3

from scripts.database import (
    count_duplicates,
    count_nulls,
    count_rows,
    table_exists
)


def test_table_exists_returns_true():

    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE airports (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """
    )

    result = table_exists(
        "airports",
        connection
    )

    connection.close()

    assert result is True

def test_table_exists_returns_false():

    connection = sqlite3.connect(":memory:")

    result = table_exists(
        "airports",
        connection
    )

    connection.close()

    assert result is False

def test_count_nulls_returns_correct_number():

    connection = sqlite3.connect(":memory:")

    connection.execute(
        """
        CREATE TABLE airports (
            id INTEGER,
            municipality TEXT
        )
        """
    )

    connection.execute(
        """
        INSERT INTO airports
        VALUES
            (1, 'Rome'),
            (2, NULL),
            (3, NULL),
            (4, 'Paris')
        """
    )

    connection.commit()

    result = count_nulls(
        "airports",
        "municipality",
        connection
    )

    connection.close()

    assert result == 2


def test_count_duplicates_returns_correct_number():

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
            (2, 'Airport B'),
            (2, 'Airport C'),
            (3, 'Airport D')
        """
    )

    connection.commit()

    result = count_duplicates(
        "airports",
        "id",
        connection
    )

    connection.close()

    assert result == 1


def test_count_rows_returns_correct_number():

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
            (2, 'Airport B'),
            (3, 'Airport C')
        """
    )

    connection.commit()

    result = count_rows(
        "airports",
        connection
    )

    connection.close()

    assert result == 3