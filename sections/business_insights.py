import streamlit as st


def show_business_insights(
    airports,
    filtered_airports,
    runways,
    frequencies
):

    st.subheader("Business Insights")

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
            f"The country with the most airports is {top_country['iso_country']} "
            f"with {top_country['number_of_airports']} airports."
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
            f"The most common airport type is {top_type['type']} "
            f"with {top_type['number_of_airports']} airports."
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

    if len(runway_stats) > 0:
        longest_runway_airport = (
            runway_stats
            .sort_values("max_runway_length", ascending=False)
            .iloc[0]
        )

        st.warning(
            f"The airport with the longest runway is "
            f"{longest_runway_airport['name']} "
            f"({longest_runway_airport['ident']}) "
            f"with a runway length of "
            f"{longest_runway_airport['max_runway_length']} ft."
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
            f"The airport with the highest number of radio frequencies is "
            f"{most_frequencies_airport['name']} "
            f"({most_frequencies_airport['ident']}) "
            f"with {most_frequencies_airport['number_of_frequencies']} frequencies."
        )

    type_elevation = (
        airports
        .groupby("type", as_index=False)
        .agg(
            average_elevation=("elevation_ft", "mean")
        )
        .sort_values("average_elevation", ascending=False)
    )

    if len(type_elevation) > 0:
        highest_elevation_type = type_elevation.iloc[0]

        st.success(
            f"The airport type with the highest average elevation is "
            f"{highest_elevation_type['type']} "
            f"with an average elevation of "
            f"{round(highest_elevation_type['average_elevation'], 2)} ft."
        )
