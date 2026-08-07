import streamlit as st

from sections.airport_types import show_airport_types
from data_loader import load_table
from filters import create_sidebar_filters

airports = load_table("airports")


st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_airport_types(
    airports,
    filtered_airports
)
