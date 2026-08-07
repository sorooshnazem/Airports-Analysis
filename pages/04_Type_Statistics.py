import streamlit as st

from sections.type_statistics import show_type_statistics
from data_loader import load_table
from filters import create_sidebar_filters

airports = load_table("airports")


st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_type_statistics(
    filtered_airports
)
