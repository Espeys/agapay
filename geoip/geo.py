import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

response = reader.city('172.20.0.11')

print(response.country)