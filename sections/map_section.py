import streamlit as st


def show_map(filtered_airports):

    st.subheader("Airport Map")

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

    map_data = map_data.rename(columns={
        "latitude_deg": "lat",
        "longitude_deg": "lon"
    })

    if len(map_data) > 0:

        st.map(
            map_data
        )

    else:

        st.warning(
            "No geographic data available for selected filters."
        )
