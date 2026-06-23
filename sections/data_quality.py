import streamlit as st


def show_data_quality(airports):

    st.subheader("Data Quality Analysis")

    missing_report = (
        airports
        .isna()
        .sum()
        .reset_index()
    )

    missing_report.columns = [
        "column_name",
        "missing_values"
    ]

    missing_report["missing_percentage"] = (
        missing_report["missing_values"] / len(airports) * 100
    )

    missing_report = missing_report.sort_values(
        "missing_values",
        ascending=False
    )

    st.dataframe(
        missing_report
    )

    st.subheader("Top Columns with Missing Values")

    top_missing = missing_report.head(10)

    st.bar_chart(
        top_missing.set_index("column_name")["missing_values"]
    )

    columns_with_missing = missing_report[
        missing_report["missing_values"] > 0
    ]

    if len(columns_with_missing) > 0:

        st.warning(
            f"There are {len(columns_with_missing)} columns with missing values."
        )

    else:

        st.success(
            "No missing values found."
        )
