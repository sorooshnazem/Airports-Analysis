import streamlit as st


def show_search_airport(airports):

    st.subheader("Search Airport")

    search_text = st.text_input(
        "Search airport by name"
    )

    if search_text:

        search_result = airports[
            airports["name"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

        st.write(
            f"Results found: {len(search_result)}"
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

    else:

        st.info(
            "Type an airport name to search."
        )
