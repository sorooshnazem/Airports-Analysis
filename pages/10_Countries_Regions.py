import streamlit as st

from sections.countries_regions import show_countries_regions
from data_loader import load_table
from filters import create_sidebar_filters

airports = load_table("airports")
countries = load_table("countries")
regions = load_table("regions")

st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_countries_regions(
    filtered_airports,
    countries,
    regions
)
