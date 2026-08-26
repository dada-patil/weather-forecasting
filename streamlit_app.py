import streamlit as st
import requests


API_URL = "http://127.0.0.1:8001"


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Weather Forecasting",
    page_icon="🌦️",
    layout="wide"
)


# =========================================
# TITLE
# =========================================

st.title("🌦️ Weather Forecasting Application")

st.write(
    "Live Weather + CRUD Management System"
)


# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("Menu")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Live Weather",
        "Create Weather",
        "View Records",
        "Update Weather",
        "Delete Weather"
    ]
)


# =========================================
# LIVE WEATHER
# =========================================

if menu == "Live Weather":

    st.header("🌍 Live Weather")

    city = st.text_input(
        "Enter City Name",
        placeholder="Example: Hyderabad"
    )

    if st.button("Get Weather"):

        if city.strip() == "":

            st.warning(
                "Please enter a city."
            )

        else:

            try:

                response = requests.get(
                    f"{API_URL}/weather/city/{city}",
                    timeout=10
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success(
                        f"Weather for {data['city']}"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Temperature",
                            f"{data['temperature']} °C"
                        )

                    with col2:

                        st.metric(
                            "Humidity",
                            f"{data['humidity']} %"
                        )

                    with col3:

                        st.metric(
                            "Wind Speed",
                            f"{data['wind_speed']} km/h"
                        )

                    st.subheader(
                        f"Condition: {data['condition']}"
                    )

                    # Forecast

                    forecast = data.get(
                        "forecast",
                        {}
                    )

                    if forecast:

                        st.subheader(
                            "📅 7-Day Forecast"
                        )

                        dates = forecast.get(
                            "time",
                            []
                        )

                        max_temp = forecast.get(
                            "temperature_2m_max",
                            []
                        )

                        min_temp = forecast.get(
                            "temperature_2m_min",
                            []
                        )

                        for i in range(
                            len(dates)
                        ):

                            st.write(
                                f"**{dates[i]}** | "
                                f"Min: {min_temp[i]}°C | "
                                f"Max: {max_temp[i]}°C"
                            )

                else:

                    st.error(
                        response.text
                    )

            except Exception as e:

                st.error(
                    f"Connection error: {e}"
                )


# =========================================
# CREATE
# =========================================

elif menu == "Create Weather":

    st.header("➕ Add Weather Record")

    city = st.text_input("City")

    temperature = st.number_input(
        "Temperature",
        value=25.0
    )

    humidity = st.number_input(
        "Humidity",
        value=50.0
    )

    wind_speed = st.number_input(
        "Wind Speed",
        value=10.0
    )

    condition = st.text_input(
        "Condition",
        value="Sunny"
    )

    if st.button("Add Record"):

        data = {

            "city": city,

            "temperature": temperature,

            "humidity": humidity,

            "wind_speed": wind_speed,

            "condition": condition
        }

        response = requests.post(
            f"{API_URL}/weather",
            json=data
        )

        if response.status_code == 200:

            st.success(
                "Weather record added successfully!"
            )

        else:

            st.error(
                response.text
            )


# =========================================
# VIEW
# =========================================

elif menu == "View Records":

    st.header("📋 Weather Records")

    response = requests.get(
        f"{API_URL}/weather"
    )

    if response.status_code == 200:

        records = response.json()

        if records:

            st.dataframe(
                records,
                use_container_width=True
            )

        else:

            st.info(
                "No records found."
            )

    else:

        st.error(
            response.text
        )


# =========================================
# UPDATE
# =========================================

elif menu == "Update Weather":

    st.header("✏️ Update Weather")

    weather_id = st.number_input(
        "Weather ID",
        min_value=1,
        step=1
    )

    temperature = st.number_input(
        "New Temperature",
        value=25.0
    )

    humidity = st.number_input(
        "New Humidity",
        value=50.0
    )

    wind_speed = st.number_input(
        "New Wind Speed",
        value=10.0
    )

    condition = st.text_input(
        "New Condition",
        value="Sunny"
    )

    if st.button("Update Record"):

        data = {

            "temperature": temperature,

            "humidity": humidity,

            "wind_speed": wind_speed,

            "condition": condition
        }

        response = requests.put(
            f"{API_URL}/weather/{weather_id}",
            json=data
        )

        if response.status_code == 200:

            st.success(
                "Record updated successfully!"
            )

        else:

            st.error(
                response.text
            )


# =========================================
# DELETE
# =========================================

elif menu == "Delete Weather":

    st.header("🗑️ Delete Weather")

    weather_id = st.number_input(
        "Weather ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Record"):

        response = requests.delete(
            f"{API_URL}/weather/{weather_id}"
        )

        if response.status_code == 200:

            st.success(
                "Record deleted successfully!"
            )

        else:

            st.error(
                response.text
            )