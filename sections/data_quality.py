import streamlit as st


def show_data_quality(airports):

    st.header("Data Quality Analysis")

    st.markdown(
        """
        This section evaluates the completeness of the airport dataset.

        It identifies missing values for each column and provides a general
        overview of data quality before performing further analyses.
        """
    )

    st.divider()

    st.subheader("Quick Summary")

    st.markdown(
        f"""
The dataset contains **{len(airports):,} airport records**.

This page measures missing values and missing percentages for every column
to help evaluate dataset completeness.
"""
    )

    st.divider()

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

    missing_report = (
        missing_report
        .sort_values(
            "missing_values",
            ascending=False
        )
    )

    columns_with_missing = (
        missing_report[
            missing_report["missing_values"] > 0
        ]
    )

    st.subheader("Data Quality Metrics")

    col1, col2 = st.columns(2)

    col1.metric(
        "Dataset Rows",
        f"{len(airports):,}"
    )

    col2.metric(
        "Columns with Missing Values",
        len(columns_with_missing)
    )

    st.divider()

    st.subheader("Missing Values Report")

    st.caption(
        """
This table summarizes the number and percentage of missing values
for every column in the dataset.
"""
    )

    st.dataframe(
        missing_report
    )

    st.subheader("Top Columns with Missing Values")

    top_missing = missing_report.head(10)

    if len(top_missing) > 0:

        st.bar_chart(
            top_missing
            .set_index("column_name")["missing_values"]
        )

    else:

        st.info(
            "No missing value information available."
        )

    st.subheader("Key Insights")

    if len(columns_with_missing) > 0:

        worst_column = columns_with_missing.iloc[0]

        st.warning(
            f"""
The column with the highest number of missing values is
**{worst_column['column_name']}**,
with **{worst_column['missing_values']:,} missing values**
(**{worst_column['missing_percentage']:.2f}%**).
"""
        )

        st.info(
            f"""
The dataset contains **{len(columns_with_missing)} columns**
with at least one missing value.
"""
        )

    else:

        st.success(
            "Excellent! No missing values were found in the dataset."
        )