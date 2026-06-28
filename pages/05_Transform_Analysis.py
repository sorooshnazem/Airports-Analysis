import streamlit as st

from sections.transform_analysis import show_transform_analysis
from data_loader import load_all_data


airports, runways, frequencies, countries, regions = load_all_data()


st.title("Airport Business Intelligence Dashboard")

filtered_airports = airports.copy()

show_transform_analysis(
    filtered_airports
)
