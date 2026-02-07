import pandas as pd
import requests as r
import matplotlib.dates as mdates
from matplotlib import pyplot as plt


def get_coordinates(dataset, city_name, country_code):
    base_url = "https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets"
    url = f"{base_url}/{dataset}/records"
    params = {
        "limit": 20,
        "where": f"place_name:'{city_name}' AND country_code:'{country_code}'"
    }

    response = r.get(url, params=params)
    data = response.json()

    if data["total_count"] == 0:
        print("Город не найден")
        exit()

    latitude = data["results"][0]["coordinates"]["lat"]
    longitude = data["results"][0]["coordinates"]["lon"]

    return latitude, longitude


def get_weather(latitude, longitude, start_date, end_date):
    weather_url = "https://archive-api.open-meteo.com/v1/archive"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }

    weather_response = r.get(weather_url, params=weather_params)
    weather_data = weather_response.json()

    return weather_data


def make_plot(weather_data, city_name):
    temp_dates = weather_data["hourly"]["time"]
    temp_values = weather_data["hourly"]["temperature_2m"]

    table = pd.DataFrame(list(zip(temp_dates, temp_values)), columns=["date", "temp"])
    table["date"] = pd.to_datetime(table["date"])

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.plot(table['date'], table['temp'])
    plt.xlabel("Даты")
    plt.ylabel("Температуры (°C)")
    plt.title(f"График температуры в {city_name}")
    plt.show()


def main():
    start_date = "2026-01-07"
    end_date = "2026-02-07"
    dataset = "geonames-postal-code@public"
    city_name = "Минск"
    country_code = "BY"
    latitude, longitude = get_coordinates(dataset, city_name, country_code)
    print(f"Координаты: {latitude}, {longitude}")

    weather_data = get_weather(latitude, longitude, start_date, end_date)

    make_plot(weather_data, city_name)


if __name__ == '__main__':
    main()