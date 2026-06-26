import streamlit as st


def show_type_statistics(filtered_airports):

    st.header("Airport Type Statistics")

    st.markdown(
        """
        This section compares airport categories using descriptive statistics.

        It provides information about airport distribution, elevation and
        country coverage for each airport type.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
        The current filtered dataset contains **{len(filtered_airports):,} airports**.

        Use this page to compare airport categories based on the number of airports,
        average elevation and geographical coverage.
        """
    )

    st.divider()

    st.subheader("Type Statistics Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Airport Types After Filters",
        filtered_airports["type"].nunique()
    )

    col2.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    st.divider()

    type_stats = (
        filtered_airports
        .groupby("type")
        .agg(
            number_of_airports=("id", "size"),
            average_elevation=("elevation_ft", "mean"),
            min_elevation=("elevation_ft", "min"),
            max_elevation=("elevation_ft", "max"),
            number_of_countries=("iso_country", "nunique")
        )
        .reset_index()
        .sort_values("number_of_airports", ascending=False)
    )

    st.caption(
        "This table summarizes each airport type using count, elevation statistics and country coverage."
    )
    st.dataframe(type_stats)

    if len(type_stats) > 0:
        st.bar_chart(
            type_stats.set_index("type")["average_elevation"]
        )
    else:
        st.info("No type statistics available for selected filters.")


    st.subheader("Key Insights")

    if len(type_stats) > 0:

        most_common_type = (
            type_stats
            .sort_values("number_of_airports", ascending=False)
            .iloc[0]
        )

        highest_elevation = (
            type_stats
            .sort_values("average_elevation", ascending=False)
            .iloc[0]
        )

        st.success(
            f"""
    The most common airport type is **{most_common_type['type']}**,
    with **{most_common_type['number_of_airports']:,} airports**.
    """
        )

        st.info(
            f"""
    The airport type with the highest average elevation is
    **{highest_elevation['type']}**, with an average elevation of
    **{highest_elevation['average_elevation']:.0f} ft**.
    """
        )

    else:

        st.warning(
            "No airport statistics are available for the selected filters."
        )
