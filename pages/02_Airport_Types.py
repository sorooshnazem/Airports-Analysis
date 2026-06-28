import streamlit as st

from sections.airport_types import show_airport_types
from data_loader import load_all_data
from filters import create_sidebar_filters

airports, runways, frequencies, countries, regions = load_all_data()


st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_airport_types(
    airports,
    filtered_airports
)
