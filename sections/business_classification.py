import streamlit as st


def classify_airport(row):

    if row["type"] == "large_airport" and row["scheduled_service"] == "yes":
        return "Strategic Hub"

    elif row["type"] == "medium_airport" and row["scheduled_service"] == "yes":
        return "Regional Airport"

    elif row["type"] == "small_airport":
        return "Local Airport"

    else:
        return "Other Infrastructure"


def show_business_classification(filtered_airports):

    st.header("Business Classification")

    st.markdown(
        """
        This section classifies airports according to simple business rules.

        The objective is to transform technical airport information into
        business-oriented categories that are easier to understand.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
The current filtered dataset contains **{len(filtered_airports):,} airports**.

Each airport is assigned to a business category based on its airport type
and scheduled passenger service.
"""
    )

    st.divider()

    airports_business = filtered_airports.copy()

    airports_business["business_category"] = airports_business.apply(
        classify_airport,
        axis=1
    )

    st.subheader("Business Classification Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Airports After Filters",
        f"{len(filtered_airports):,}"
    )

    col2.metric(
        "Business Categories",
        airports_business["business_category"].nunique()
    )

    st.divider()

    st.subheader("Airport Business Categories")

    st.caption(
        """
This table shows the business category assigned to each airport
according to the implemented classification rules.
"""
    )

    st.dataframe(
        airports_business[
            [
                "ident",
                "name",
                "type",
                "scheduled_service",
                "business_category"
            ]
        ].head(100)
    )

    business_category_count = (
        airports_business
        .groupby("business_category", as_index=False)
        .size()
        .rename(columns={"size": "number_of_airports"})
        .sort_values("number_of_airports", ascending=False)
    )

    st.subheader("Number of Airports by Business Category")

    if len(business_category_count) > 0:

        st.dataframe(
            business_category_count
        )

        st.bar_chart(
            business_category_count
            .set_index("business_category")["number_of_airports"]
        )

    else:

        st.info(
            "No business classification data available."
        )

    st.subheader("Key Insights")

    if len(business_category_count) > 0:

        top_category = business_category_count.iloc[0]

        st.success(
            f"""
The most common business category is
**{top_category['business_category']}**,
with **{top_category['number_of_airports']:,} airports**.
"""
        )

        strategic_hubs = len(
            airports_business[
                airports_business["business_category"] == "Strategic Hub"
            ]
        )

        st.info(
            f"""
The current filtered dataset contains
**{strategic_hubs:,} Strategic Hub airports**.
"""
        )

    else:

        st.warning(
            "No business insights available for the selected filters."
        )