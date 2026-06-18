import streamlit as st


def show_type_statistics(filtered_airports):

    st.subheader("Airport Type Statistics")

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

    st.dataframe(type_stats)

    if len(type_stats) > 0:
        st.bar_chart(
            type_stats.set_index("type")["average_elevation"]
        )
    else:
        st.info("No type statistics available for selected filters.")
