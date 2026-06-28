import streamlit as st

from sections.top_countries import show_top_countries
from data_loader import load_all_data

airports, runways, frequencies, countries, regions = load_all_data()


st.title("Airport Business Intelligence Dashboard")

show_top_countries(
    airports
)
