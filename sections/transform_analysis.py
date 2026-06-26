import streamlit as st


def show_transform_analysis(filtered_airports):

    st.header("Elevation Comparison Analysis")

    st.markdown(
        """
        This section compares each airport elevation with the average elevation
        of airports belonging to the same type.

        It helps identify which airports are above or below the typical elevation
        of their category.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
            f"""
    The current filtered dataset contains **{len(filtered_airports):,} airports**.

    This analysis uses the airport type as the comparison group and calculates
    how far each airport is from the average elevation of its own category.
    """
    )

    st.divider()

    st.subheader("Elevation Comparison Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    col2.metric(
        "Airport Types After Filters",
        filtered_airports["type"].nunique()
    )

    st.divider()

    st.subheader("Airports Compared to Type Average")

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

    st.caption(
        """
    Interpretation:

    - A positive difference means the airport is located above the average elevation
      of airports with the same type.

    - A negative difference means the airport is located below the average elevation
      of its category.
    """
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
    ]
    .sort_values(
        "difference_from_type_average",
        ascending=False
    )
    .head(100)
)

    st.subheader("Key Insights")

    if len(airports_transform) > 0:

        above_count = airports_transform["is_above_type_average"].sum()

        below_or_equal_count = (
            len(airports_transform) - above_count
        )

        st.success(
            f"""
    There are **{above_count:,} airports** above the average elevation
    of their airport type.
    """
        )

        st.info(
            f"""
    There are **{below_or_equal_count:,} airports** below or equal to
    the average elevation of their airport type.
    """
        )

    else:

        st.warning(
            "No elevation comparison data available for the selected filters."
        )
