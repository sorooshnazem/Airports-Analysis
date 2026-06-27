import streamlit as st


def show_countries_regions(
    filtered_airports,
    countries_df,
    regions
):

    st.header("Countries and Regions Analysis")

    st.markdown(
        """
        This section enriches airport information with country and region names.

        It provides a geographical overview of airport distribution and
        allows users to compare countries and administrative regions.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
The current filtered dataset contains **{len(filtered_airports):,} airports**.

This page combines airport, country and region datasets to produce
geographical reports and regional statistics.
"""
    )

    st.divider()

    countries_clean = countries_df[
        ["code", "name"]
    ].rename(columns={
        "code": "country_code",
        "name": "country_name"
    })

    regions_clean = regions[
        ["code", "name"]
    ].rename(columns={
        "code": "region_code",
        "name": "region_name"
    })

    airports_countries = filtered_airports.merge(
        countries_clean,
        left_on="iso_country",
        right_on="country_code",
        how="left"
    )

    st.subheader("Countries & Regions Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    col2.metric(
        "Countries",
        airports_countries["country_name"].nunique()
    )

    st.divider()

    st.subheader("Airports with Country Names")

    st.caption(
        """
This table enriches airport information with the corresponding country names.
"""
    )

    st.dataframe(
        airports_countries[
            [
                "id",
                "ident",
                "name",
                "type",
                "iso_country",
                "country_name",
                "municipality"
            ]
        ].head(100)
    )

    country_report = (
        airports_countries
        .groupby(["iso_country", "country_name"], as_index=False)
        .agg(
            number_of_airports=("id", "size"),
            average_elevation=("elevation_ft", "mean"),
            number_of_airport_types=("type", "nunique")
        )
        .sort_values("number_of_airports", ascending=False)
        .head(20)
    )

    st.subheader("Top Countries")

    if len(country_report) > 0:

        st.dataframe(country_report)

        st.bar_chart(
            country_report
            .set_index("country_name")["number_of_airports"]
        )

    else:

        st.info(
            "No country data available for the selected filters."
        )

    airports_countries_regions = airports_countries.merge(
        regions_clean,
        left_on="iso_region",
        right_on="region_code",
        how="left"
    )

    st.subheader("Airports with Country and Region Names")

    st.caption(
        """
This table enriches airports with both country and administrative region names.
"""
    )

    st.dataframe(
        airports_countries_regions[
            [
                "id",
                "ident",
                "name",
                "type",
                "iso_country",
                "country_name",
                "iso_region",
                "region_name",
                "municipality"
            ]
        ].head(100)
    )

    region_report = (
        airports_countries_regions
        .groupby(["iso_region", "region_name"], as_index=False)
        .agg(
            number_of_airports=("id", "size"),
            average_elevation=("elevation_ft", "mean"),
            number_of_countries=("iso_country", "nunique")
        )
        .sort_values("number_of_airports", ascending=False)
        .head(20)
    )

    st.subheader("Top Regions")

    if len(region_report) > 0:

        st.dataframe(region_report)

        st.bar_chart(
            region_report
            .set_index("region_name")["number_of_airports"]
        )

    else:

        st.info(
            "No region data available for the selected filters."
        )

    st.subheader("Key Insights")

    if len(country_report) > 0:

        top_country = country_report.iloc[0]

        st.success(
            f"""
The country with the highest number of airports is
**{top_country['country_name']}**
with **{top_country['number_of_airports']:,} airports**.
"""
        )

    if len(region_report) > 0:

        top_region = region_report.iloc[0]

        st.info(
            f"""
The region with the highest number of airports is
**{top_region['region_name']}**
with **{top_region['number_of_airports']:,} airports**.
"""
        )

    if len(country_report) == 0 and len(region_report) == 0:

        st.warning(
            "No geographical insights available for the selected filters."
        )