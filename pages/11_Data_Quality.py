import streamlit as st

from sections.data_quality import show_data_quality
from data_loader import load_all_data

airports, runways, frequencies, countries, regions = load_all_data()


st.title("Airport Business Intelligence Dashboard")

show_data_quality(
    airports
)
