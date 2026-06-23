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

    st.subheader("Business Airport Classification")

    airports_business = filtered_airports.copy()

    airports_business["business_category"] = airports_business.apply(
        classify_airport,
        axis=1
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

    st.dataframe(business_category_count)

    if len(business_category_count) > 0:
        st.bar_chart(
            business_category_count
            .set_index("business_category")["number_of_airports"]
        )
    else:
        st.info("No business classification data available.")
