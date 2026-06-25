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

    info_col, goals_col = st.columns(2)

    with info_col:

        st.subheader("Project Information")

        st.metric(
            "Version",
            "1.1"
        )

        st.metric(
            "Data Source",
            "OurAirports"
        )

        st.metric(
            "Update",
            "Daily"
        )

    with goals_col:

        st.subheader("Project Goals")

        st.markdown(
            """
    - Explore worldwide airport infrastructure.

    - Analyze airports, runways and radio frequencies.

    - Demonstrate how open data can be transformed into a business dashboard.
    """
        )

    st.divider()

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

    st.divider()

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

    st.divider()

    st.subheader("Key Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Airports", f"{len(airports):,}")
        st.metric("Airport Types", airports["type"].nunique())

    with col2:
        st.metric("Total Countries", airports["iso_country"].nunique())
        st.metric("Airports After Filters", f"{len(filtered_airports):,}")

    st.divider()

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

    st.divider()

    st.subheader("Dashboard Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            """
            **Airport Analytics**

            - Airport Types
            - Top Countries
            - Type Statistics
            - Elevation Analysis
            """
        )

    with col2:
        st.info(
            """
            **Infrastructure**

            - Runways
            - Frequencies
            - Countries & Regions
            - Map
            """
        )

    with col3:
        st.info(
            """
            **Business & Quality**

            - Search Airports
            - Business Classification
            - Business Insights
            - Data Quality
            """
        )