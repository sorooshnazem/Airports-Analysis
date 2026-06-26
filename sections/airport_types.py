import streamlit as st


def show_airport_types(
    airports,
    filtered_airports
):
    st.header("Airport Types Analysis")

    st.markdown(
            """
            This section analyzes the distribution of airports by type.

            It helps users understand which airport categories are most common globally
            and how the selected filters affect the distribution.
            """
        )

    st.divider()

    st.subheader("Quick Summary")

    airport_types = airports["type"].nunique()

    st.markdown(
        f"""
    The dataset contains **{airport_types} different airport types**.

    Use this page to compare the global distribution of airport categories
    and evaluate how the selected filters modify the results.
    """
    )


    st.subheader("Airport Type Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Global Airport Types",
        airports["type"].nunique()
    )

    col2.metric(
        "Filtered Airport Types",
        filtered_airports["type"].nunique()
    )

    st.divider()

    st.subheader("Global Airport Type Distribution")

    st.caption(
        "This chart uses the full dataset and is not affected by sidebar filters."
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
        .reset_index(drop=True)
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

    st.subheader("Airport Type Distribution After Filters")

    st.caption(
        "This chart changes based on the filters selected in the sidebar."
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


    st.subheader("Key Insights")

    if len(filtered_airports) > 0:

        top_type = (
            filtered_airports["type"]
            .value_counts()
            .idxmax()
        )

        top_count = (
            filtered_airports["type"]
            .value_counts()
            .max()
        )

        st.success(
            f"""
    The most common airport type after applying the current filters is
    **{top_type}**, with **{top_count:,} airports**.
    """
        )

    else:

        st.warning(
            "No airports available for the selected filters."
        )
