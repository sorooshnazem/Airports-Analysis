import streamlit as st

st.set_page_config(
    page_title="Airport BI Dashboard",
    page_icon="✈️",
    layout="wide"
)

st.title("Airport Business Intelligence Dashboard")

st.markdown(
    """
    Welcome to the Airport Business Intelligence Dashboard.

    Use the pages in the sidebar to explore airport data, runway infrastructure,
    frequencies, countries, regions, data quality, business insights and maps.
    """
)