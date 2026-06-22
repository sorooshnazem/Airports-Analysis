import pandas as pd
import streamlit as st
from sections.overview import show_overview
from sections.airport_types import show_airport_types
from sections.top_countries import show_top_countries
from sections.type_statistics import show_type_statistics
from sections.runways import show_runways

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

    st.subheader("Airport Elevation Compared to Type Average")

    airports_transform = filtered_airports.copy()

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

    st.subheader("Airport Frequencies Analysis")

    airport_frequencies = filtered_airports.merge(
        frequencies,
        left_on="id",
        right_on="airport_ref",
        how="inner"
    )

    st.dataframe(
        airport_frequencies[
            [
                "ident",
                "name",
                "type_x",
                "iso_country",
                "airport_ident",
                "type_y",
                "description",
                "frequency_mhz"
            ]
        ].head(100)
    )

    frequency_stats = (
        airport_frequencies
        .groupby(["ident", "name"], as_index=False)
        .agg(
            number_of_frequencies=("frequency_mhz", "size"),
            min_frequency=("frequency_mhz", "min"),
            max_frequency=("frequency_mhz", "max"),
            number_of_frequency_types=("type_y", "nunique")
        )
        .sort_values("number_of_frequencies", ascending=False)
    )

    st.subheader("Top Airports by Number of Frequencies")

    top_frequency_airports = frequency_stats.head(20)

    st.dataframe(top_frequency_airports)

    if len(top_frequency_airports) > 0:
        st.bar_chart(
            top_frequency_airports.set_index("ident")["number_of_frequencies"]
        )


# -----------------------------
# SEARCH
# -----------------------------

elif page == "Search":

    st.subheader("Search Airport")

    search_text = st.text_input("Search airport by name")

    if search_text:
        search_result = airports[
            airports["name"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        st.write(f"Results found: {len(search_result)}")

        st.dataframe(
            search_result[
                [
                    "ident",
                    "name",
                    "type",
                    "iso_country",
                    "municipality",
                    "scheduled_service"
                ]
            ]
        )

    else:
        st.info("Type an airport name to search.")


# -----------------------------
# BUSINESS CLASSIFICATION
# -----------------------------

elif page == "Business Classification":

    st.subheader("Business Airport Classification")

    airports_business = filtered_airports.copy()

    airports_business["business_category"] = airports_business.apply(
        classify_airport,
        axis=1
    )

    st.dataframe(
        airports_business[
            [
                "ident",
                "name",
                "type",
                "scheduled_service",
                "business_category"
            ]
        ].head(100)
    )

    business_category_count = (
        airports_business
        .groupby("business_category", as_index=False)
        .size()
        .rename(columns={"size": "number_of_airports"})
        .sort_values("number_of_airports", ascending=False)
    )

    st.subheader("Number of Airports by Business Category")

    st.dataframe(business_category_count)

    if len(business_category_count) > 0:
        st.bar_chart(
            business_category_count.set_index("business_category")[
                "number_of_airports"
            ]
        )


# -----------------------------
# COUNTRIES AND REGIONS
# -----------------------------

elif page == "Countries and Regions":

    st.subheader("Countries and Regions Analysis")

    countries_clean = countries_df[
        ["code", "name"]
    ].rename(columns={
        "code": "country_code",
        "name": "country_name"
    })

    regions_clean = regions[
        ["code", "name"]
    ].rename(columns={
        "code": "region_code",
        "name": "region_name"
    })

    airports_countries = filtered_airports.merge(
        countries_clean,
        left_on="iso_country",
        right_on="country_code",
        how="left"
    )

    st.subheader("Airports with Country Names")

    st.dataframe(
        airports_countries[
            [
                "id",
                "ident",
                "name",
                "type",
                "iso_country",
                "country_name",
                "municipality"
            ]
        ].head(100)
    )

    country_report = (
        airports_countries
        .groupby(["iso_country", "country_name"], as_index=False)
        .agg(
            number_of_airports=("id", "size"),
            average_elevation=("elevation_ft", "mean"),
            number_of_airport_types=("type", "nunique")
        )
        .sort_values("number_of_airports", ascending=False)
        .head(20)
    )

    st.subheader("Top Countries with Full Names")

    st.dataframe(country_report)

    if len(country_report) > 0:
        st.bar_chart(
            country_report.set_index("country_name")["number_of_airports"]
        )

    airports_countries_regions = airports_countries.merge(
        regions_clean,
        left_on="iso_region",
        right_on="region_code",
        how="left"
    )

    st.subheader("Airports with Country and Region Names")

    st.dataframe(
        airports_countries_regions[
            [
                "id",
                "ident",
                "name",
                "type",
                "iso_country",
                "country_name",
                "iso_region",
                "region_name",
                "municipality"
            ]
        ].head(100)
    )

    region_report = (
        airports_countries_regions
        .groupby(["iso_region", "region_name"], as_index=False)
        .agg(
            number_of_airports=("id", "size"),
            average_elevation=("elevation_ft", "mean"),
            number_of_countries=("iso_country", "nunique")
        )
        .sort_values("number_of_airports", ascending=False)
        .head(20)
    )

    st.subheader("Top Regions by Number of Airports")

    st.dataframe(region_report)

    if len(region_report) > 0:
        st.bar_chart(
            region_report.set_index("region_name")["number_of_airports"]
        )


# -----------------------------
# DATA QUALITY
# -----------------------------

elif page == "Data Quality":

    st.subheader("Data Quality Analysis")

    missing_report = (
        airports
        .isna()
        .sum()
        .reset_index()
    )

    missing_report.columns = [
        "column_name",
        "missing_values"
    ]

    missing_report["missing_percentage"] = (
        missing_report["missing_values"] / len(airports) * 100
    )

    missing_report = missing_report.sort_values(
        "missing_values",
        ascending=False
    )

    st.dataframe(missing_report)

    st.subheader("Top Columns with Missing Values")

    top_missing = missing_report.head(10)

    st.bar_chart(
        top_missing.set_index("column_name")["missing_values"]
    )

    columns_with_missing = missing_report[
        missing_report["missing_values"] > 0
    ]

    if len(columns_with_missing) > 0:
        st.warning(
            f"There are {len(columns_with_missing)} columns with missing values."
        )
    else:
        st.success("No missing values found.")


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