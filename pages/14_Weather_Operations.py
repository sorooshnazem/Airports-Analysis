import streamlit as st

from data_loader import load_table


st.title("Weather Operations Monitoring")

weather = load_table(
    "airport_weather"
)

if weather.empty:
    st.warning("No weather data available.")
    st.stop()

airport_name = weather.loc[0, "airport_name"]
airport_ident = weather.loc[0, "airport_ident"]
weather_time = weather.loc[0, "weather_time"]

st.subheader(
    f"{airport_name} ({airport_ident})"
)

st.caption(
    f"Weather observation time: {weather_time}"
)

st.subheader(
    "Current weather data"
)

st.dataframe(
    weather
)

st.subheader("Operational Weather Summary")

temperature = weather.loc[0, "temperature_c"]
precipitation = weather.loc[0, "precipitation_mm"]
wind_speed = weather.loc[0, "wind_speed_kmh"]
wind_gusts = weather.loc[0, "wind_gusts_kmh"]
priority = weather.loc[0, "monitoring_priority"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Temperature",
    f"{temperature} °C"
)

col2.metric(
    "Precipitation",
    f"{precipitation} mm"
)

col3.metric(
    "Wind Speed",
    f"{wind_speed} km/h"
)

col4.metric(
    "Wind Gusts",
    f"{wind_gusts} km/h"
)

st.metric(
    "Monitoring Priority",
    priority
)

runways = load_table(
    "runways"
)

airport_runways = runways[
    runways["airport_ident"] == airport_ident
]

st.subheader(
    "Runway Context"
)

if airport_runways.empty:

    st.warning(
        "No runway data available for this airport."
    )

else:

    number_of_runways = len(
        airport_runways
    )

    max_runway_length = (
        airport_runways["length_ft"]
        .max()
    )

    lighted_runways = (
        airport_runways["lighted"]
        .sum()
    )

    closed_runways = (
        airport_runways["closed"]
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Runways",
        number_of_runways
    )

    col2.metric(
        "Longest Runway",
        f"{max_runway_length:.0f} ft"
    )

    col3.metric(
        "Lighted Runways",
        int(lighted_runways)
    )

    col4.metric(
        "Closed Runways",
        int(closed_runways)
    )

    st.subheader("Operational Context")

    if priority == "High":

        st.warning(
            "Weather conditions currently require high monitoring attention. "
            "Review wind, precipitation and runway availability."
        )

    elif priority == "Medium":

        st.info(
            "Weather conditions require moderate monitoring attention. "
            "Runway infrastructure should be considered together with current wind conditions."
        )

    else:

        st.success(
            "Current weather conditions show a low monitoring priority "
            "according to the dashboard rules."
        )

    if closed_runways > 0:

        st.warning(
            f"{int(closed_runways)} runway(s) are currently marked as closed."
        )

    else:

        st.write(
            "No runways are currently marked as closed in the dataset."
        )