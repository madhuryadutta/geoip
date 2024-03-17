import geoip2.database
import json

# IP address to lookup
ip_address = "104.28.216.196"
print(type(ip_address))
exit()
# Path to the GeoIP2 City ,Country,ASN database file
city_database_path = "../db/GeoLite2-City.mmdb"
country_database_path = "../db/GeoLite2-Country.mmdb"
asn_database_path = "../db/GeoLite2-ASN.mmdb"


# Initialize reader object named reader_city ,reader_country ,reader_asn
reader_city = geoip2.database.Reader(city_database_path)
reader_country = geoip2.database.Reader(country_database_path)
reader_asn = geoip2.database.Reader(asn_database_path)

try:
    # Perform the lookup
    response = reader_city.city(ip_address)
    print("Country Name:", response.country.name)
    print("Country ISO Code:", response.country.iso_code)
    print("Region:", response.subdivisions.most_specific.name)
    print("City:", response.city.name)
    print("Latitude:", response.location.latitude)
    print("Longitude:", response.location.longitude)
    print("Postal Code:", response.postal.code)
    print("Time Zone:", response.location.time_zone)

except geoip2.errors.AddressNotFoundError:
    print("Address not found in the database")
finally:
    # Close the reader
    reader_city.close()
try:
    # Perform the lookup
    response = reader_country.country(ip_address)

    print("Continent:", response.continent.code)
    print("Continent:", response.continent.names)
except geoip2.errors.AddressNotFoundError:
    print("Address not found in the database")
finally:
    # Close the reader
    reader_country.close()

try:
    # Perform the lookup
    response = reader_asn.asn(ip_address)

    print("ASN:", response.autonomous_system_number)
    print("ASN Organization:", response.autonomous_system_organization)
except geoip2.errors.AddressNotFoundError:
    print("Address not found in the database")
finally:
    # Close the reader
    reader_asn.close()
