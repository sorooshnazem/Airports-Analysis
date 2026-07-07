import streamlit as st

from sections.transform_analysis import show_transform_analysis
from data_loader import load_table


airports = load_table("airports")

st.title("Airport Business Intelligence Dashboard")

filtered_airports = airports.copy()

show_transform_analysis(
    filtered_airports
)
