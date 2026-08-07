import pandas as pd
import streamlit as st
import sqlite3

from scripts.config import DATABASE_FILE


@st.cache_data
def load_table(table_name):
    connection = sqlite3.connect(DATABASE_FILE)

    dataframe = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        connection
    )

    connection.close()

    return dataframe
