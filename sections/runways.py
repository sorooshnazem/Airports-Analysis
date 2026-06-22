import streamlit as st


def show_runways(filtered_airports, runways):

    st.subheader("Runway Analysis")

    airport_runways = filtered_airports.merge(
        runways,
        left_on="id",
        right_on="airport_ref",
        how="inner"
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
