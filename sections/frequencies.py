import streamlit as st


def show_frequencies(filtered_airports, frequencies):

    st.subheader("Airport Frequencies Analysis")

    airport_frequencies = filtered_airports.merge(
        frequencies,
        left_on="id",
        right_on="airport_ref",
        how="inner"
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
