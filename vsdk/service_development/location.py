"""
This module contains the current location handlers for the weather service.

Usage:
```
from .location import get_location

location = get_location()
latitude = location.latitude
longitude = location.longitude
```

"""

import requests
import gpsd

class LocationException(Exception):
    """Exception thrown when module couldn't obtain coordinates"""
    pass


class Location:
    """Class holding Latitude and Longitude pair"""

    def __init__(self, latitude, longitude):
        self._latitude = latitude
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        try:
            _lat = float(value)
        except ValueError:
            raise LocationException("Latitude could not be parsed: {}".format(value))
        else:
            if not -90 < _lat < 90:
                raise LocationException("Latitude not in valid range")
            else:
                self._latitude = _lat

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        try:
            _long = float(value)
        except ValueError:
            raise LocationException("Longitude could not be parsed: {}".format(value))
        else:
            if not -180 < _long < 180:
                raise LocationException("Longitude not in valid range")
            else:
                self._longitude = _long

    def __str__(self):
        return 'latitude: {}  longitude: {}'.format(self.latitude, self.longitude)


def get_location():
    """Module interface to return the location of the computer.
    Tries first to get GPS coordinates, then tries to get location via its public IP address.
    """

    try:
        return _get_gps()
    except Exception:
        print("Getting location via GPS failed, trying via public IP address...")
        try:
            return _get_ip()
        except Exception:
            raise LocationException("Getting location via IP address failed!")


def _get_gps():
    """Module-internal function to fetch location via GPS.
    Requires `gpsd` installed properly on the RPi.
    """
    gpsd.connect()
    packet = gpsd.get_current()
    return Location(longitude=packet.lon, latitude=packet.lat)


def _get_ip():
    """Module-internal function to fetch location via Public IP address"""
    r = requests.get('https://get.geojs.io/v1/ip/geo.json', timeout=1)
    r.raise_for_status()
    data = r.json()
    return Location(longitude=data['longitude'], latitude=data['latitude'])


if __name__ == '__main__':
    location = get_location()
    print(location)
