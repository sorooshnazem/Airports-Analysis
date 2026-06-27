import streamlit as st


def show_map(filtered_airports):

    st.header("Airport Map")

    st.markdown(
        """
        This section visualizes the geographical distribution of airports.

        The interactive map displays all airports available after applying
        the current filters.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
The current filtered dataset contains **{len(filtered_airports):,} airports**.

Only airports with valid latitude and longitude coordinates are displayed
on the map.
"""
    )

    st.divider()

    map_data = filtered_airports[
        [
            "latitude_deg",
            "longitude_deg",
            "name",
            "type",
            "iso_country"
        ]
    ].dropna(
        subset=[
            "latitude_deg",
            "longitude_deg"
        ]
    )

    map_data = map_data.rename(
        columns={
            "latitude_deg": "lat",
            "longitude_deg": "lon"
        }
    )

    st.subheader("Map Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    col2.metric(
        "Airports on Map",
        f"{len(map_data):,}"
    )

    st.divider()

    st.subheader("Airport Geographic Distribution")

    st.caption(
        """
The map shows all airports with valid geographic coordinates.
Zoom and move the map to explore different regions.
"""
    )

    if len(map_data) > 0:

        st.map(
            map_data
        )

    else:

        st.warning(
            "No geographic data available for the selected filters."
        )

    st.subheader("Key Insights")

    if len(map_data) > 0:

        countries = map_data["iso_country"].nunique()

        airport_types = map_data["type"].nunique()

        st.success(
            f"""
The current map displays **{len(map_data):,} airports**
distributed across **{countries} countries**.
"""
        )

        st.info(
            f"""
The displayed airports belong to
**{airport_types} different airport types**.
"""
        )

    else:

        st.warning(
            "No geographic insights available."
        )