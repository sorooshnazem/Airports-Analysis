import streamlit as st

from sections.business_classification import show_business_classification
from data_loader import load_all_data
from filters import create_sidebar_filters

airports, runways, frequencies, countries, regions = load_all_data()


st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_business_classification(
    filtered_airports
)
