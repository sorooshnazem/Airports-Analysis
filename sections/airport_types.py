import streamlit as st


def show_airport_types(
    airports,
    filtered_airports
):

    st.subheader(
        "Number of Airports by Type - Global"
    )

    airports_by_type = (
        airports
        .groupby("type", as_index=False)
        .size()
        .rename(columns={
            "size": "number_of_airports"
        })
        .sort_values(
            "number_of_airports",
            ascending=False
        )
    )

    st.dataframe(
        airports_by_type
    )

    st.bar_chart(
        airports_by_type
        .set_index("type")[
            "number_of_airports"
        ]
    )

    st.subheader(
        "Airport Types After Filters"
    )

    airport_types_filtered = (
        filtered_airports
        .groupby("type", as_index=False)
        .size()
        .rename(columns={
            "size": "number_of_airports"
        })
        .sort_values(
            "number_of_airports",
            ascending=False
        )
    )

    st.dataframe(
        airport_types_filtered
    )

    if len(
        airport_types_filtered
    ) > 0:

        st.bar_chart(
            airport_types_filtered
            .set_index("type")[
                "number_of_airports"
            ]
        )

    else:

        st.info(
            "No data available for selected filters."
        )
