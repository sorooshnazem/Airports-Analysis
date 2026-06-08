import pandas as pd
import streamlit as st

st.title("Airport Business Intelligence Dashboard")

airports = pd.read_csv("data/airports.csv")

countries = sorted(
    airports["iso_country"]
    .dropna()
    .unique()
)

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

selected_country = st.sidebar.selectbox(
    "Select Country",
    countries
)

filtered_airports = airports[
    airports["iso_country"] == selected_country
]

st.subheader("Selected Country")

st.write(
    f"Number of airports: {len(filtered_airports)}"
)

st.dataframe(
    filtered_airports[
        [
            "ident",
            "name",
            "type",
            "municipality"
        ]
    ]
)

st.metric(
    "Airports in Country",
    len(filtered_airports)
)

country_types = (
    filtered_airports
    .groupby("type", as_index=False)
    .size()
    .rename(columns={"size": "number_of_airports"})
)

st.subheader("Airport Types in Selected Country")

st.dataframe(country_types)

st.bar_chart(
    country_types.set_index("type")["number_of_airports"]
)

st.subheader("Top Countries by Number of Airports")

top_countries = (
    airports
    .groupby("iso_country", as_index=False)
    .size()
    .rename(columns={"size": "number_of_airports"})
    .sort_values("number_of_airports", ascending=False)
    .head(10)
)

st.dataframe(top_countries)

st.bar_chart(
    top_countries.set_index("iso_country")["number_of_airports"]
)

st.subheader("Airport Type Statistics")

type_stats = (
    airports
    .groupby("type")
    .agg(
        number_of_airports=("id", "size"),
        average_elevation=("elevation_ft", "mean"),
        min_elevation=("elevation_ft", "min"),
        max_elevation=("elevation_ft", "max"),
        number_of_countries=("iso_country", "nunique")
    )
    .reset_index()
    .sort_values("number_of_airports", ascending=False)
)

st.dataframe(type_stats)

st.bar_chart(
    type_stats.set_index("type")["average_elevation"]
)

st.subheader("Airport Elevation Compared to Type Average")

airports_transform = airports.copy()

airports_transform["average_elevation_by_type"] = (
    airports_transform
    .groupby("type")["elevation_ft"]
    .transform("mean")
)

airports_transform["difference_from_type_average"] = (
    airports_transform["elevation_ft"]
    - airports_transform["average_elevation_by_type"]
)

airports_transform["is_above_type_average"] = (
    airports_transform["elevation_ft"]
    > airports_transform["average_elevation_by_type"]
)

show_only_above = st.checkbox(
    "Show only airports above type average elevation"
)

if show_only_above:
    airports_transform = airports_transform[
        airports_transform["is_above_type_average"] == True
    ]

st.dataframe(
    airports_transform[
        [
            "ident",
            "name",
            "type",
            "elevation_ft",
            "average_elevation_by_type",
            "difference_from_type_average",
            "is_above_type_average"
        ]
    ].head(100)
)