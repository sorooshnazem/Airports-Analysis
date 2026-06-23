import pandas as pd
import streamlit as st
from sections.overview import show_overview
from sections.airport_types import show_airport_types
from sections.top_countries import show_top_countries
from sections.type_statistics import show_type_statistics
from sections.runways import show_runways
from sections.transform_analysis import show_transform_analysis
from sections.frequencies import show_frequencies
from sections.search_airport import show_search_airport
from sections.business_classification import show_business_classification
from sections.countries_regions import show_countries_regions
from sections.data_quality import show_data_quality

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        st.stop()
    except Exception as error:
        st.error(f"Error while loading file: {file_path}")
        st.write(error)
        st.stop()


def classify_airport(row):
    if row["type"] == "large_airport" and row["scheduled_service"] == "yes":
        return "Strategic Hub"
    elif row["type"] == "medium_airport" and row["scheduled_service"] == "yes":
        return "Regional Airport"
    elif row["type"] == "small_airport":
        return "Local Airport"
    else:
        return "Other Infrastructure"


st.title("Airport Business Intelligence Dashboard")

airports = load_csv("data/airports.csv")
runways = load_csv("data/runways.csv")
frequencies = load_csv("data/airport-frequencies.csv")
countries_df = load_csv("data/countries.csv")
regions = load_csv("data/regions.csv")

# -----------------------------
# PAGE NAVIGATION
# -----------------------------

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Airport Types",
        "Top Countries",
        "Type Statistics",
        "Transform Analysis",
        "Runways",
        "Frequencies",
        "Search",
        "Business Classification",
        "Countries and Regions",
        "Data Quality",
        "Business Insights",
        "Map"
    ]
)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Dashboard Filters")

countries = sorted(airports["iso_country"].dropna().unique())
country_options = ["All"] + countries

selected_country = st.sidebar.selectbox(
    "Select Country",
    country_options
)

airport_types = sorted(airports["type"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Select Airport Type",
    airport_types,
    default=airport_types
)

scheduled_options = ["All"] + sorted(
    airports["scheduled_service"].dropna().unique()
)

selected_scheduled = st.sidebar.selectbox(
    "Scheduled Service",
    scheduled_options
)

filtered_airports = airports.copy()

if selected_country != "All":
    filtered_airports = filtered_airports[
        filtered_airports["iso_country"] == selected_country
    ]

filtered_airports = filtered_airports[
    filtered_airports["type"].isin(selected_types)
]

if selected_scheduled != "All":
    filtered_airports = filtered_airports[
        filtered_airports["scheduled_service"] == selected_scheduled
    ]


# -----------------------------
# OVERVIEW
# -----------------------------

if page == "Overview":

    show_overview(
        airports,
        filtered_airports
    )


# -----------------------------
# AIRPORT TYPES
# -----------------------------

elif page == "Airport Types":

    show_airport_types(
        airports,
        filtered_airports
    )


# -----------------------------
# TOP COUNTRIES
# -----------------------------

elif page == "Top Countries":

    show_top_countries(
        airports
    )

# -----------------------------
# TYPE STATISTICS
# -----------------------------

elif page == "Type Statistics":

    show_type_statistics(
        filtered_airports
    )


# -----------------------------
# TRANSFORM ANALYSIS
# -----------------------------

elif page == "Transform Analysis":

    show_transform_analysis(
        filtered_airports
    )


# -----------------------------
# RUNWAYS
# -----------------------------

elif page == "Runways":

    show_runways(
        filtered_airports,
        runways
    )


# -----------------------------
# FREQUENCIES
# -----------------------------

elif page == "Frequencies":

    show_frequencies(
        filtered_airports,
        frequencies
    )

# -----------------------------
# SEARCH
# -----------------------------

elif page == "Search":

    show_search_airport(
        airports
    )


# -----------------------------
# BUSINESS CLASSIFICATION
# -----------------------------

elif page == "Business Classification":

    show_business_classification(
        filtered_airports
    )


# -----------------------------
# COUNTRIES AND REGIONS
# -----------------------------

elif page == "Countries and Regions":

    show_countries_regions(
        filtered_airports,
        countries_df,
        regions
    )

# -----------------------------
# DATA QUALITY
# -----------------------------

elif page == "Data Quality":

    show_data_quality(
        airports
    )


# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------

elif page == "Business Insights":

    st.subheader("Business Insights")

    country_airport_count = (
        airports
        .groupby("iso_country", as_index=False)
        .size()
        .rename(columns={"size": "number_of_airports"})
        .sort_values("number_of_airports", ascending=False)
    )

    if len(country_airport_count) > 0:
        top_country = country_airport_count.iloc[0]

        st.success(
            f"The country with the most airports is {top_country['iso_country']} "
            f"with {top_country['number_of_airports']} airports."
        )

    type_airport_count = (
        airports
        .groupby("type", as_index=False)
        .size()
        .rename(columns={"size": "number_of_airports"})
        .sort_values("number_of_airports", ascending=False)
    )

    if len(type_airport_count) > 0:
        top_type = type_airport_count.iloc[0]

        st.info(
            f"The most common airport type is {top_type['type']} "
            f"with {top_type['number_of_airports']} airports."
        )

    airport_runways = filtered_airports.merge(
        runways,
        left_on="id",
        right_on="airport_ref",
        how="inner"
    )

    runway_stats = (
        airport_runways
        .groupby(["ident", "name"], as_index=False)
        .agg(
            number_of_runways=("airport_ref", "size"),
            max_runway_length=("length_ft", "max")
        )
    )

    if len(runway_stats) > 0:
        longest_runway_airport = (
            runway_stats
            .sort_values("max_runway_length", ascending=False)
            .iloc[0]
        )

        st.warning(
            f"The airport with the longest runway is "
            f"{longest_runway_airport['name']} "
            f"({longest_runway_airport['ident']}) "
            f"with a runway length of "
            f"{longest_runway_airport['max_runway_length']} ft."
        )

    airport_frequencies = filtered_airports.merge(
        frequencies,
        left_on="id",
        right_on="airport_ref",
        how="inner"
    )

    frequency_stats = (
        airport_frequencies
        .groupby(["ident", "name"], as_index=False)
        .agg(
            number_of_frequencies=("frequency_mhz", "size")
        )
    )

    if len(frequency_stats) > 0:
        most_frequencies_airport = (
            frequency_stats
            .sort_values("number_of_frequencies", ascending=False)
            .iloc[0]
        )

        st.info(
            f"The airport with the highest number of radio frequencies is "
            f"{most_frequencies_airport['name']} "
            f"({most_frequencies_airport['ident']}) "
            f"with {most_frequencies_airport['number_of_frequencies']} frequencies."
        )

    type_elevation = (
        airports
        .groupby("type", as_index=False)
        .agg(
            average_elevation=("elevation_ft", "mean")
        )
        .sort_values("average_elevation", ascending=False)
    )

    if len(type_elevation) > 0:
        highest_elevation_type = type_elevation.iloc[0]

        st.success(
            f"The airport type with the highest average elevation is "
            f"{highest_elevation_type['type']} "
            f"with an average elevation of "
            f"{round(highest_elevation_type['average_elevation'], 2)} ft."
        )


# -----------------------------
# MAP
# -----------------------------

elif page == "Map":

    st.subheader("Airport Map")

    map_data = filtered_airports[
        [
            "latitude_deg",
            "longitude_deg",
            "name",
            "type",
            "iso_country"
        ]
    ].dropna(subset=["latitude_deg", "longitude_deg"])

    map_data = map_data.rename(columns={
        "latitude_deg": "lat",
        "longitude_deg": "lon"
    })

    if len(map_data) > 0:
        st.map(map_data)
    else:
        st.warning("No geographic data available for selected filters.")