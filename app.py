import pandas as pd
import streamlit as st

st.title("Airport Business Intelligence Dashboard")

airports = pd.read_csv("data/airports.csv")

st.subheader("Airports Dataset Preview")
st.dataframe(airports.head())

total_airports = len(airports)
total_countries = airports["iso_country"].nunique()
total_types = airports["type"].nunique()

st.metric("Total Airports", total_airports)
st.metric("Total Countries", total_countries)
st.metric("Airport Types", total_types)

airports_by_type = (
    airports.groupby("type", as_index=False)
    .size()
    .rename(columns={"size": "number_of_airports"})
)

st.subheader("Number of Airports by Type")
st.dataframe(airports_by_type)

st.bar_chart(
    airports_by_type.set_index("type")["number_of_airports"]
)