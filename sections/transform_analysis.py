import streamlit as st


def show_transform_analysis(filtered_airports):

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
