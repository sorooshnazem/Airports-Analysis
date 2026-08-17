import sqlite3

import pandas as pd
import streamlit as st

from scripts.build_database import main
from scripts.config import DATABASE_FILE


def ensure_database_ready():

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='airports'
        """
    )

    table = cursor.fetchone()

    connection.close()

    if table is None:
        main(
            include_weather=False
        )


@st.cache_data
def load_table(table_name):

    ensure_database_ready()

    connection = sqlite3.connect(DATABASE_FILE)

    dataframe = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        connection
    )

    connection.close()

    return dataframe