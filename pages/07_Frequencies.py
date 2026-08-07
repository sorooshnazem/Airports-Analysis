import streamlit as st

from sections.frequencies import show_frequencies
from data_loader import load_table
from filters import create_sidebar_filters

airports = load_table("airports")
frequencies = load_table("frequencies")


st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_frequencies(
    filtered_airports,
    frequencies
)
