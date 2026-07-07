import streamlit as st

from sections.search_airport import show_search_airport
from data_loader import load_table
from filters import create_sidebar_filters

airports = load_table("airports")

st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_search_airport(
    airports
)
