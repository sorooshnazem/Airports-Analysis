import streamlit as st

from sections.business_insights import show_business_insights
from data_loader import load_table
from filters import create_sidebar_filters

airports = load_table("airports")
runways = load_table("runways")
frequencies = load_table("frequencies")

st.title("Airport Business Intelligence Dashboard")

filtered_airports = create_sidebar_filters(airports)

show_business_insights(
    airports,
    filtered_airports,
    runways,
    frequencies
)
