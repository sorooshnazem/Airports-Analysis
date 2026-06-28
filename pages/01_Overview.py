import streamlit as st
from sections.overview import show_overview
from filters import create_sidebar_filters
from data_loader import load_all_data

airports, runways, frequencies, countries, regions = load_all_data()

filtered_airports = create_sidebar_filters(airports)


st.title("Airport Business Intelligence Dashboard")

show_overview(
    airports,
    filtered_airports
)