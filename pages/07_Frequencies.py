import streamlit as st

from sections.frequencies import show_frequencies
from data_loader import load_all_data
from filters import create_sidebar_filters

airports, runways, frequencies, countries, regions = load_all_data()


st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_frequencies(
    filtered_airports,
    frequencies
)
