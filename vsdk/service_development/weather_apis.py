from datetime import datetime

import requests
from abc import ABC, abstractmethod

class WeatherForecast:
    """Weather forecast for multiple WeatherForecastDay"""

    def __init__(self, days):
        self.days = days

    def __repr__(self):
        return str(self.days)

class WeatherForecastDay:
    """Weather forecast for one day"""

    def __init__(self, forecast_date, wind_speed, rainfall):
        self._forecast_date = forecast_date
        self._wind_speed = wind_speed
        self._rainfall = rainfall

    @property
    def forecast_date(self):
        return self._forecast_date

    @forecast_date.setter
    def forecast_date(self, value):
        self._forecast_date = value

    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, value):
        self._wind_speed = float(value)

    @property
    def rainfall(self):
        return self._rainfall

    @rainfall.setter
    def rainfall(self, value):
        self._rainfall = float(value)

    def __repr__(self):
        return '<WeatherForecastDay date={} wind_speed={} rainfall={}>'.format(self.forecast_date, self.wind_speed, self.rainfall)


class WeatherAPI(ABC):

    def __init__(self, api_key):

        self.api_key = api_key
        super().__init__()

    @abstractmethod
    def get_forecast(self, location):
        pass


class OpenWeatherMapAPI(WeatherAPI):

    def get_forecast(self, location):
        """Method to get forecast. Must return an instance of class WeatherForecast"""
        # https://openweathermap.org/api/one-call-api
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s'
            % (location.latitude, location.longitude, self.api_key)
        ).json()

        days = list()
        # assumes ordered list from API
        for day in response['daily']:
            wfd = WeatherForecastDay(
                forecast_date=datetime.utcfromtimestamp(int(day['dt'])).date(),
                wind_speed=day['wind_speed'],
                rainfall=day.get('rain', 0)
            )
            days.append(wfd)

        forecast = WeatherForecast(days)
        return forecast

def get_apis(api_key):
    return OpenWeatherMapAPI(api_key)
        
    


