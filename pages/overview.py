import streamlit as st


def show_overview(airports, filtered_airports):

    st.subheader("Airports Dataset Preview")

    st.dataframe(
        airports.head()
    )

    st.metric(
        "Total Airports",
        len(airports)
    )

    st.metric(
        "Total Countries",
        airports["iso_country"].nunique()
    )

    st.metric(
        "Airport Types",
        airports["type"].nunique()
    )

    st.metric(
        "Airports After Filters",
        len(filtered_airports)
    )

    st.subheader("Filtered Airports")

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
