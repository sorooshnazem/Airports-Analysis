import streamlit as st


def show_search_airport(airports):

    st.header("Airport Search")

    st.markdown(
        """
        This section allows users to search airports by name.

        The search is case-insensitive and returns all airports whose names
        contain the text entered by the user.
        """
    )

    st.divider()

    st.subheader("Search Criteria")

    search_text = st.text_input(
        "Airport Name"
    )

    st.divider()

    if search_text:

        search_result = airports[
            airports["name"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        st.subheader("Search Results")

        col1, col2 = st.columns(2)

        col1.metric(
            "Results Found",
            len(search_result)
        )

        col2.metric(
            "Search Text",
            search_text
        )

        if len(search_result) > 0:

            st.caption(
                "The table below shows all airports matching the search criteria."
            )

            st.dataframe(
                search_result[
                    [
                        "ident",
                        "name",
                        "type",
                        "iso_country",
                        "municipality",
                        "scheduled_service"
                    ]
                ]
            )

            st.subheader("Key Insights")

            airport_types = (
                search_result["type"]
                .nunique()
            )

            countries = (
                search_result["iso_country"]
                .nunique()
            )

            st.success(
                f"""
The search returned **{len(search_result):,} airports**
distributed across **{countries} countries**
and **{airport_types} airport types**.
"""
            )

        else:

            st.warning(
                "No airports match the search criteria."
            )

    else:

        st.info(
            "Enter an airport name to start searching."
        )