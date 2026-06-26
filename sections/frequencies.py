import streamlit as st


def show_frequencies(filtered_airports, frequencies):

    st.header("Radio Frequencies Analysis")

    st.markdown(
        """
        This section analyzes airport radio frequency information.

        It helps users identify airports with more communication records,
        frequency ranges and different types of radio communication.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
        The current filtered dataset contains **{len(filtered_airports):,} airports**.

        This page combines airport data with radio frequency information to analyze
        communication services, frequency ranges and airport communication infrastructure.
        """
    )

    st.divider()

    airport_frequencies = filtered_airports.merge(
        frequencies,
        left_on="id",
        right_on="airport_ref",
        how="inner"
    )

    st.subheader("Frequency Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    col2.metric(
        "Frequency Records",
        f"{len(airport_frequencies):,}"
    )

    st.divider()

    st.subheader("Airport Frequency Dataset")

    st.caption(
        """
        This table shows airports matched with their radio frequency records.
        Each airport can have multiple communication frequencies.
        """
    )

    st.dataframe(
        airport_frequencies[
            [
                "ident",
                "name",
                "type_x",
                "iso_country",
                "airport_ident",
                "type_y",
                "description",
                "frequency_mhz"
            ]
        ].head(100)
    )

    frequency_stats = (
        airport_frequencies
        .groupby(["ident", "name"], as_index=False)
        .agg(
            number_of_frequencies=("frequency_mhz", "size"),
            min_frequency=("frequency_mhz", "min"),
            max_frequency=("frequency_mhz", "max"),
            number_of_frequency_types=("type_y", "nunique")
        )
        .sort_values("number_of_frequencies", ascending=False)
    )

    st.subheader("Top Airports by Number of Frequencies")

    top_frequency_airports = frequency_stats.head(20)

    st.dataframe(top_frequency_airports)

    if len(top_frequency_airports) > 0:
        st.bar_chart(
            top_frequency_airports.set_index("ident")["number_of_frequencies"]
        )
    else:
        st.info("No frequency data available for selected filters.")

    st.subheader("Key Insights")

    if len(frequency_stats) > 0:

        airport_most_frequencies = (
            frequency_stats
            .sort_values("number_of_frequencies", ascending=False)
            .iloc[0]
        )

        st.success(
            f"""
            The airport with the highest number of radio frequencies is
            **{airport_most_frequencies["name"]}**
            with **{airport_most_frequencies["number_of_frequencies"]:,} frequency records**.
            """
        )

        frequency_stats_valid = frequency_stats.dropna(
            subset=["max_frequency"]
        )

        if len(frequency_stats_valid) > 0:

            highest_frequency_airport = (
                frequency_stats_valid
                .sort_values("max_frequency", ascending=False)
                .iloc[0]
            )

            st.info(
                f"""
                The airport with the highest recorded radio frequency is
                **{highest_frequency_airport["name"]}**
                with a maximum frequency of
                **{highest_frequency_airport["max_frequency"]:.3f} MHz**.
                """
            )

        else:

            st.warning(
                "No valid frequency information available for the selected filters."
            )

    else:

        st.warning(
            "No frequency insights available for the selected filters."
        )