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

    st.subheader("Sample of Filtered Airports")

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
        ].head(100)
    )