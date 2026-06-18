import streamlit as st


def show_top_countries(airports):

    st.subheader(
        "Top Countries by Number of Airports"
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
