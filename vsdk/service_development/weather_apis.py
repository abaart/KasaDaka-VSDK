import abc
import requests
from abc import ABC, abstractmethod

class WeatherAPI(ABC):

    def __init__(self, api_key):

        self.api_key = api_key
        super().__init__()

    @abstractmethod
    def get_wind_speed(self):
        pass


class OpenWeatherMapAPI(WeatherAPI):

    def get_wind_speed(self, location):

        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s'
            % (location.latitude, location.longitude, self.api_key)
        ).json()
        
        return response['wind']['speed']


def get_apis(api_key):
    return OpenWeatherMapAPI(api_key)
        
    


