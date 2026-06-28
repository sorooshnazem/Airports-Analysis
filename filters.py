import streamlit as st


def create_sidebar_filters(airports):

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

    return filtered_airports
