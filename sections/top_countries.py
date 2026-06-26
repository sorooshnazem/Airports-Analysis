import streamlit as st


def show_top_countries(airports):

    st.header("Top Countries Analysis")

    st.markdown(
        """
        This section highlights the countries with the highest number of airports.

        It helps users understand where airport infrastructure is most concentrated
        at a global level.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    total_countries = airports["iso_country"].nunique()

    st.markdown(
        f"""
    The dataset contains airports from **{total_countries} countries**.

    This page ranks countries by the total number of airports available in the dataset.
    """
    )

    st.divider()

    st.subheader("Country Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Countries in Dataset",
        airports["iso_country"].nunique()
    )

    col2.metric(
        "Airports in Dataset",
        f"{len(airports):,}"
    )

    st.divider()

    st.subheader(
        "Top 10 Countries by Number of Airports"
        )

    st.caption(
    "This ranking is based on the complete airport dataset and is not affected by sidebar filters."
    )

    top_countries = (
        airports
        .groupby(
            "iso_country",
            as_index=False
        )
        .size()
        .rename(
            columns={
                "size": "number_of_airports"
            }
        )
        .sort_values(
            "number_of_airports",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_countries
    )

    st.bar_chart(
        top_countries
        .set_index("iso_country")[
            "number_of_airports"
        ]
    )

    st.subheader("Key Insights")

    if len(top_countries) > 0:

        top_country = top_countries.iloc[0]

        st.success(
            f"""
    The country with the highest number of airports is
    **{top_country["iso_country"]}**, with **{top_country["number_of_airports"]:,} airports**.
    """
        )

    else:

        st.warning(
            "No country data available."
        )
