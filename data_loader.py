import pandas as pd
import streamlit as st
import sqlite3


DATABASE_PATH = "database/airports.db"


@st.cache_data
def load_table(table_name):
    connection = sqlite3.connect(DATABASE_PATH)

    dataframe = pd.read_sql_query(
        f"SELECT * FROM {table_name}",
        connection
    )

    connection.close()

    return dataframe
