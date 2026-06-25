import streamlit as st


def show_overview(airports, filtered_airports):

    st.header("Dashboard Overview")

    st.markdown(
        """
        Welcome to the **Airport Business Intelligence Dashboard**.

        This dashboard helps users explore global airport infrastructure using
        open aviation data. It provides insights about airport distribution,
        airport types, runways, radio frequencies, countries, regions,
        data quality, and business-oriented classifications.
        """
    )

    st.info(
        """
        **Data Source:** OurAirports open dataset.

        The data is updated regularly through an automated GitHub Actions workflow.
        """
    )

    st.subheader("Project Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Version",
            "1.1"
        )

    with col2:

        st.metric(
            "Data Source",
            "OurAirports"
        )

    with col3:

        st.metric(
            "Last Update",
            "Automatic"
        )

    st.subheader("Project Goals")

    st.markdown(
        """
        This project has three main goals:

        - Provide a clear business view of worldwide airport infrastructure.
        - Help users explore airport, runway, frequency, country and region data interactively.
        - Demonstrate how open data can be transformed into a useful analytical dashboard.
        """
    )

    st.subheader("How to Use This Dashboard")

    st.markdown(
        """
        Use the sidebar to navigate between different analysis pages and apply filters.

        Recommended exploration flow:

        1. Start from the global overview.
        2. Explore airport types and top countries.
        3. Analyze infrastructure using runways and frequencies.
        4. Check business insights and data quality.
        5. Use the map to explore geographic distribution.
        """
    )
    st.subheader("About this Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            ### Airport Analytics

            - Airport Types
            - Top Countries
            - Airport Statistics
            - Elevation Analysis
            - Search Airports
            """
        )

    with col2:
        st.markdown(
            """
            ### Infrastructure & Business

            - Runway Analysis
            - Radio Frequencies
            - Countries & Regions
            - Business Insights
            - Interactive Map
            """
        )

    st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Airports", len(airports))
    col2.metric("Total Countries", airports["iso_country"].nunique())
    col3.metric("Airport Types", airports["type"].nunique())
    col4.metric("Airports After Filters", len(filtered_airports))

    st.subheader("Airport Types Overview")

    airports_by_type = (
        airports
        .groupby("type", as_index=False)
        .size()
        .rename(columns={"size": "number_of_airports"})
        .sort_values("number_of_airports", ascending=False)
    )

    st.bar_chart(
        airports_by_type.set_index("type")["number_of_airports"]
    )

    st.subheader("Dashboard Modules")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            """
    Airport Analysis

    - Airport Types
    - Top Countries
    - Type Statistics
    - Search Airports
    """
        )

    with col2:

        st.success(
            """
    Infrastructure Analysis

    - Runways
    - Frequencies
    - Countries & Regions
    - Business Insights
    - Map
    """
        )