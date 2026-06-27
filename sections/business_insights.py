import streamlit as st


def show_business_insights(
    airports,
    filtered_airports,
    runways,
    frequencies
):

    st.header("Business Insights")

    st.markdown(
        """
        This section automatically generates high-level insights from the data.

        It summarizes key information about airport distribution, airport types,
        runway infrastructure, radio frequencies and elevation patterns.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
The full dataset contains **{len(airports):,} airports**.

The current filtered dataset contains **{len(filtered_airports):,} airports**.
These insights help users quickly understand the most important patterns
without manually reading every table.
"""
    )

    st.divider()

    st.subheader("Insight Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Airports",
        f"{len(airports):,}"
    )

    col2.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    st.divider()

    st.subheader("Generated Insights")

    country_airport_count = (
        airports
        .groupby("iso_country", as_index=False)
        .size()
        .rename(columns={"size": "number_of_airports"})
        .sort_values("number_of_airports", ascending=False)
    )

    if len(country_airport_count) > 0:
        top_country = country_airport_count.iloc[0]

        st.success(
            f"""
The country with the most airports is
**{top_country['iso_country']}**
with **{top_country['number_of_airports']:,} airports**.
"""
        )

    type_airport_count = (
        airports
        .groupby("type", as_index=False)
        .size()
        .rename(columns={"size": "number_of_airports"})
        .sort_values("number_of_airports", ascending=False)
    )

    if len(type_airport_count) > 0:
        top_type = type_airport_count.iloc[0]

        st.info(
            f"""
The most common airport type is
**{top_type['type']}**
with **{top_type['number_of_airports']:,} airports**.
"""
        )

    airport_runways = filtered_airports.merge(
        runways,
        left_on="id",
        right_on="airport_ref",
        how="inner"
    )

    runway_stats = (
        airport_runways
        .groupby(["ident", "name"], as_index=False)
        .agg(
            number_of_runways=("airport_ref", "size"),
            max_runway_length=("length_ft", "max")
        )
    )

    runway_stats_with_length = runway_stats.dropna(
        subset=["max_runway_length"]
    )

    if len(runway_stats_with_length) > 0:
        longest_runway_airport = (
            runway_stats_with_length
            .sort_values("max_runway_length", ascending=False)
            .iloc[0]
        )

        st.warning(
            f"""
The airport with the longest runway is
**{longest_runway_airport['name']}**
({longest_runway_airport['ident']})
with a runway length of
**{longest_runway_airport['max_runway_length']:,.0f} ft**.
"""
        )

    airport_frequencies = filtered_airports.merge(
        frequencies,
        left_on="id",
        right_on="airport_ref",
        how="inner"
    )

    frequency_stats = (
        airport_frequencies
        .groupby(["ident", "name"], as_index=False)
        .agg(
            number_of_frequencies=("frequency_mhz", "size")
        )
    )

    if len(frequency_stats) > 0:
        most_frequencies_airport = (
            frequency_stats
            .sort_values("number_of_frequencies", ascending=False)
            .iloc[0]
        )

        st.info(
            f"""
The airport with the highest number of radio frequencies is
**{most_frequencies_airport['name']}**
({most_frequencies_airport['ident']})
with **{most_frequencies_airport['number_of_frequencies']:,} frequencies**.
"""
        )

    type_elevation = (
        airports
        .groupby("type", as_index=False)
        .agg(
            average_elevation=("elevation_ft", "mean")
        )
        .dropna(subset=["average_elevation"])
        .sort_values("average_elevation", ascending=False)
    )

    if len(type_elevation) > 0:
        highest_elevation_type = type_elevation.iloc[0]

        st.success(
            f"""
The airport type with the highest average elevation is
**{highest_elevation_type['type']}**
with an average elevation of
**{highest_elevation_type['average_elevation']:.0f} ft**.
"""
        )

    if (
        len(country_airport_count) == 0
        and len(type_airport_count) == 0
        and len(runway_stats_with_length) == 0
        and len(frequency_stats) == 0
        and len(type_elevation) == 0
    ):
        st.warning(
            "No business insights are available for the selected filters."
        )