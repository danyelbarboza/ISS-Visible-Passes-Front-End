import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

class OpenMeteoClient:
    def __init__(self):
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        
    def get_weather_data(self, latitude, longitude, date_time):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_hour": date_time,
            "end_hour": date_time,
            "timezone": "America/Sao_Paulo",
            "hourly": "temperature_2m,cloudcover,visibility,relative_humidity_2m,is_day"
        }
        responses = self.openmeteo.weather_api(url, params=params)

        response = responses[0]

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_cloudcover = hourly.Variables(1).ValuesAsNumpy()
        hourly_visibility = hourly.Variables(2).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(3).ValuesAsNumpy()
        hourly_is_day = hourly.Variables(4).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}

        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["cloudcover"] = hourly_cloudcover
        hourly_data["visibility"] = hourly_visibility
        hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
        hourly_data["is_day"] = hourly_is_day

        hourly_dataframe = pd.DataFrame(data = hourly_data)

        temperature_at_time = hourly_dataframe['temperature_2m'].iloc[0]
        cloudcover_at_time = hourly_dataframe['cloudcover'].iloc[0]
        visibility_at_time = hourly_dataframe['visibility'].iloc[0]
        relative_humidity_2m_at_time = hourly_dataframe['relative_humidity_2m'].iloc[0]
        is_day_at_time = hourly_dataframe['is_day'].iloc[0]
        
        
        return {
            "temperature_2m": temperature_at_time,
            "cloudcover": cloudcover_at_time,
            "visibility": visibility_at_time,
            "relative_humidity_2m": relative_humidity_2m_at_time,
            "is_day": is_day_at_time
        }