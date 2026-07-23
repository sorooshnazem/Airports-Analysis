import sqlite3
from config import DATABASE_FILE


def get_connection():

    connection = sqlite3.connect(DATABASE_FILE)

    return connection


def save_table(dataframe, table_name, connection):

    dataframe.to_sql(
        name=table_name,
        con=connection,
        if_exists="replace",
        index=False
    )

    print(f"Table '{table_name}' created.")

def count_rows(table_name, connection):

    cursor = connection.cursor()

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM {table_name}
        """
    )

    number_of_rows = cursor.fetchone()[0]

    return number_of_rows

def table_exists(table_name, connection):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (table_name,)
    )

    result = cursor.fetchone()

    return result is not None

def count_duplicates(table_name, column_name, connection):

    cursor = connection.cursor()

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM (
            SELECT {column_name}
            FROM {table_name}
            GROUP BY {column_name}
            HAVING COUNT(*) > 1
        )
        """
    )

    return cursor.fetchone()[0]


def count_nulls(table_name, column_name, connection):

    cursor = connection.cursor()

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM {table_name}
        WHERE {column_name} IS NULL
        """
    )

    return cursor.fetchone()[0]
