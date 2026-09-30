import os
import geoip2.database
from geoip2.errors import AddressNotFoundError

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "geoip",
    "GeoLite2-City.mmdb"
)

reader = geoip2.database.Reader(DB_PATH)


def get_location(ip):
    try:
        response = reader.city(ip)

        return {
            "country": response.country.name,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude
        }

    except AddressNotFoundError:
        return {
            "country": "Unknown",
            "city": "Unknown",
            "latitude": None,
            "longitude": None
        }