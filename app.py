import pandas as pd
import streamlit as st


def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data

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
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Dashboard Filters")

countries = sorted(
    airports["iso_country"]
    .dropna()
    .unique()
)

country_options = ["All"] + countries

selected_country = st.sidebar.selectbox(
    "Select Country",
    country_options
)

airport_types = sorted(
    airports["type"]
    .dropna()
    .unique()
)

selected_types = st.sidebar.multiselect(
    "Select Airport Type",
    airport_types,
    default=airport_types
)

scheduled_options = ["All"] + sorted(
    airports["scheduled_service"]
    .dropna()
    .unique()
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

st.subheader("Airports Dataset Preview")
st.dataframe(airports.head())

total_airports = len(airports)
total_countries = airports["iso_country"].nunique()
total_types = airports["type"].nunique()

st.metric("Total Airports", total_airports)
st.metric("Total Countries", total_countries)
st.metric("Airport Types", total_types)

st.metric("Airports After Filters", len(filtered_airports))


# -----------------------------
# AIRPORTS BY TYPE
# -----------------------------

airports_by_type = (
    airports.groupby("type", as_index=False)
    .size()
    .rename(columns={"size": "number_of_airports"})
)

st.subheader("Number of Airports by Type - Global")

st.dataframe(airports_by_type)

st.bar_chart(
    airports_by_type.set_index("type")["number_of_airports"]
)


# -----------------------------
# FILTERED AIRPORTS
# -----------------------------

st.subheader("Filtered Airports")

st.write(
    f"Number of airports after filters: {len(filtered_airports)}"
)

st.dataframe(
    filtered_airports[
        [
            "ident",
            "name",
            "type",
            "iso_country",
            "municipality",
            "scheduled_service"
        ]
    ].head(200)
)


# -----------------------------
# AIRPORT TYPES IN FILTERED DATA
# -----------------------------

country_types = (
    filtered_airports
    .groupby("type", as_index=False)
    .size()
    .rename(columns={"size": "number_of_airports"})
)

st.subheader("Airport Types After Filters")

st.dataframe(country_types)

if len(country_types) > 0:
    st.bar_chart(
        country_types.set_index("type")["number_of_airports"]
    )
else:
    st.info("No data available for selected filters.")


# -----------------------------
# TOP COUNTRIES
# -----------------------------

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


# -----------------------------
# AIRPORT TYPE STATISTICS
# -----------------------------

st.subheader("Airport Type Statistics")

type_stats = (
    filtered_airports
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

if len(type_stats) > 0:
    st.bar_chart(
        type_stats.set_index("type")["average_elevation"]
    )
else:
    st.info("No type statistics available for selected filters.")


# -----------------------------
# TRANSFORM ANALYSIS
# -----------------------------

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
# RUNWAY ANALYSIS
# -----------------------------

st.subheader("Runway Analysis")

airport_runways = filtered_airports.merge(
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
    ].head(100)
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

if len(top_runway_airports) > 0:
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

if len(top_length_airports) > 0:
    st.bar_chart(
        top_length_airports.set_index("ident")["max_runway_length"]
    )


# -----------------------------
# FREQUENCIES ANALYSIS
# -----------------------------

st.subheader("Airport Frequencies Analysis")

airport_frequencies = filtered_airports.merge(
    frequencies,
    left_on="id",
    right_on="airport_ref",
    how="inner"
)

st.write("Airports joined with frequencies")

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
# SEARCH AIRPORT
# -----------------------------

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
        business_category_count.set_index("business_category")["number_of_airports"]
    )


# -----------------------------
# COUNTRIES AND REGIONS ANALYSIS
# -----------------------------

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