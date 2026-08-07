def select_columns(dataframe, columns):

    return dataframe[columns].copy()

def fill_missing_text(dataframe, columns, value="Unknown"):

    dataframe_copy = dataframe.copy()

    for column in columns:
        dataframe_copy[column] = (
            dataframe_copy[column]
            .fillna(value)
        )

    return dataframe_copy


def transform_current_weather(
    weather_response,
    airport_id,
    airport_ident,
    airport_name
):

    current_weather = weather_response["current"]
    monitoring_priority = classify_weather_monitoring_priority(
        precipitation_mm=current_weather["precipitation"],
        wind_gusts_kmh=current_weather["wind_gusts_10m"]
    )

    return {
        "airport_id": airport_id,
        "airport_ident": airport_ident,
        "airport_name": airport_name,
        "weather_time": current_weather["time"],
        "temperature_c": current_weather["temperature_2m"],
        "apparent_temperature_c": (
            current_weather["apparent_temperature"]
        ),
        "precipitation_mm": current_weather["precipitation"],
        "weather_code": current_weather["weather_code"],
        "wind_speed_kmh": current_weather["wind_speed_10m"],
        "wind_direction_deg": (
            current_weather["wind_direction_10m"]
        ),
        "wind_gusts_kmh": current_weather["wind_gusts_10m"],
        "monitoring_priority": monitoring_priority
    }

def classify_weather_monitoring_priority(
    precipitation_mm,
    wind_gusts_kmh
):

    if (
        precipitation_mm >= 10
        or wind_gusts_kmh >= 60
    ):
        return "High"

    if (
        precipitation_mm >= 3
        or wind_gusts_kmh >= 40
    ):
        return "Medium"

    return "Low"
