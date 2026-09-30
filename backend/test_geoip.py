from geoip import get_location

ip = "8.8.8.8"

result = get_location(ip)

print(result)