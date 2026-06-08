import pandas as pd
import streamlit as st

st.title("Airport Business Intelligence Dashboard")

airports = pd.read_csv("data/airports.csv")
runways = pd.read_csv("data/runways.csv")

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

st.subheader("Runway Analysis")

st.write("Preview of runways dataset")
st.dataframe(runways.head())

airport_runways = airports.merge(
    runways,
    left_on="id",
    right_on="airport_ref",
    how="inner"
)

st.write("Airports joined with runways")
st.dataframe(
    airport_runways[
        [
            "ident",
            "name",
            "type",
            "iso_country",
            "airport_ident",
            "length_ft",
            "width_ft",
            "surface",
            "lighted",
            "closed"
        ]
    ].head()
)

runway_stats = (
    airport_runways
    .groupby(["ident", "name"], as_index=False)
    .agg(
        number_of_runways=("airport_ref", "size"),
        max_runway_length=("length_ft", "max"),
        average_runway_length=("length_ft", "mean"),
        average_runway_width=("width_ft", "mean"),
        number_of_lighted_runways=("lighted", "sum"),
        number_of_closed_runways=("closed", "sum")
    )
    .sort_values("number_of_runways", ascending=False)
)

st.subheader("Top Airports by Number of Runways")

top_runway_airports = runway_stats.head(20)

st.dataframe(top_runway_airports)

st.bar_chart(
    top_runway_airports.set_index("ident")["number_of_runways"]
)

st.subheader("Top Airports by Maximum Runway Length")

top_length_airports = (
    runway_stats
    .sort_values("max_runway_length", ascending=False)
    .head(20)
)

st.dataframe(top_length_airports)

st.bar_chart(
    top_length_airports.set_index("ident")["max_runway_length"]
)