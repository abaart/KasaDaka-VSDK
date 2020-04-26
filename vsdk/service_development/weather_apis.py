import abc
import requests

def get_wind_speed(api_key):
        
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?lat=13.892505&lon=-8.837564&appid=%s'
        % (api_key)
    ).json()

    return response['wind']['speed']


