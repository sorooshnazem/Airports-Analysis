import streamlit as st

from sections.runways import show_runways
from filters import create_sidebar_filters
from data_loader import load_table

airports = load_table("airports")
runways = load_table("runways")

st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_runways(
    filtered_airports,
    runways
)
