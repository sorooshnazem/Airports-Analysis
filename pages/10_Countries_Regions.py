import streamlit as st

from sections.countries_regions import show_countries_regions
from data_loader import load_all_data
from filters import create_sidebar_filters

airports, runways, frequencies, countries, regions = load_all_data()


st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_countries_regions(
    filtered_airports,
    countries,
    regions
)
