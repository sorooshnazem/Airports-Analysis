import streamlit as st

from sections.top_countries import show_top_countries
from data_loader import load_table

airports = load_table("airports")

st.title("Airport Business Intelligence Dashboard")

show_top_countries(
    airports
)
