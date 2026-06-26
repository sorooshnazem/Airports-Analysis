import streamlit as st


def show_runways(filtered_airports, runways):

    st.header("Runway Infrastructure Analysis")

    st.markdown(
        """
        This section analyzes airport runway infrastructure.

        It helps users identify airports with more developed runway systems,
        longer runways, lighted runways and closed runway infrastructure.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
        The current filtered dataset contains **{len(filtered_airports):,} airports**.

        This page connects airport data with runway data to understand runway capacity,
        runway length, lighting availability and closed runway infrastructure.
        """
    )

    st.divider()

    airport_runways = filtered_airports.merge(
        runways,
        left_on="id",
        right_on="airport_ref",
        how="inner"
    )

    st.subheader("Runway Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    col2.metric(
        "Runway Records",
        f"{len(airport_runways):,}"
    )

    st.divider()

    st.subheader("Airport Runway Dataset")

    st.caption(
        """
        This table shows airports matched with their runway records.
        Each airport can appear multiple times if it has more than one runway.
        """
    )

    st.dataframe(
        airport_runways[
            [
                "ident",
                "name",
                "type",
                "iso_country",
                "airport_ident",
                "length_ft",
                "width_ft",
                "surface",
                "lighted",
                "closed"
            ]
        ].head(100)
    )

    runway_stats = (
        airport_runways
        .groupby(["ident", "name"], as_index=False)
        .agg(
            number_of_runways=("airport_ref", "size"),
            max_runway_length=("length_ft", "max"),
            average_runway_length=("length_ft", "mean"),
            average_runway_width=("width_ft", "mean"),
            number_of_lighted_runways=("lighted", "sum"),
            number_of_closed_runways=("closed", "sum")
        )
        .sort_values("number_of_runways", ascending=False)
    )

    st.subheader("Top Airports by Number of Runways")

    top_runway_airports = runway_stats.head(20)

    st.dataframe(top_runway_airports)

    if len(top_runway_airports) > 0:
        st.bar_chart(
            top_runway_airports.set_index("ident")["number_of_runways"]
        )
    else:
        st.info("No runway data available for selected filters.")

    st.subheader("Top Airports by Maximum Runway Length")

    top_length_airports = (
        runway_stats
        .dropna(subset=["max_runway_length"])
        .sort_values("max_runway_length", ascending=False)
        .head(20)
    )

    st.dataframe(top_length_airports)

    if len(top_length_airports) > 0:
        st.bar_chart(
            top_length_airports.set_index("ident")["max_runway_length"]
        )
    else:
        st.info("No runway length data available for selected filters.")

    st.subheader("Key Insights")

    if len(runway_stats) > 0:

        airport_most_runways = (
            runway_stats
            .sort_values("number_of_runways", ascending=False)
            .iloc[0]
        )

        st.success(
            f"""
            The airport with the highest number of runways is
            **{airport_most_runways["name"]}**
            with **{airport_most_runways["number_of_runways"]:,} runways**.
            """
        )

        runway_stats_with_length = runway_stats.dropna(
            subset=["max_runway_length"]
        )

        if len(runway_stats_with_length) > 0:

            airport_longest_runway = (
                runway_stats_with_length
                .sort_values("max_runway_length", ascending=False)
                .iloc[0]
            )

            st.info(
                f"""
                The airport with the longest runway is
                **{airport_longest_runway["name"]}**
                with a maximum runway length of
                **{airport_longest_runway["max_runway_length"]:,.0f} ft**.
                """
            )

        else:

            st.warning(
                "No valid runway length data available for the selected filters."
            )

    else:

        st.warning(
            "No runway insights available for the selected filters."
        )