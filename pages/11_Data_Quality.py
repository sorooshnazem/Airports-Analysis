import streamlit as st

from sections.data_quality import show_data_quality
from data_loader import load_table

airports = load_table("airports")

st.title("Airport Business Intelligence Dashboard")

show_data_quality(
    airports
)
