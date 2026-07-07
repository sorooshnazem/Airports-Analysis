import sqlite3


DATABASE_PATH = "database/airports.db"


def get_connection():

    connection = sqlite3.connect(DATABASE_PATH)

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
