import streamlit as st


def show_countries_regions(
    filtered_airports,
    countries_df,
    regions
):

    st.subheader("Countries and Regions Analysis")

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

    st.subheader("Airports with Country Names")

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

    st.subheader("Top Countries with Full Names")

    st.dataframe(country_report)

    if len(country_report) > 0:
        st.bar_chart(
            country_report
            .set_index("country_name")["number_of_airports"]
        )
    else:
        st.info("No country data available for selected filters.")

    airports_countries_regions = airports_countries.merge(
        regions_clean,
        left_on="iso_region",
        right_on="region_code",
        how="left"
    )

    st.subheader("Airports with Country and Region Names")

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

    st.subheader("Top Regions by Number of Airports")

    st.dataframe(region_report)

    if len(region_report) > 0:
        st.bar_chart(
            region_report
            .set_index("region_name")["number_of_airports"]
        )
    else:
        st.info("No region data available for selected filters.")
