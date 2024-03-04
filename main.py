import geoip2.database
import json


# IP address to lookup
# ip_address = '106.222.227.107'
# IP address to lookup
ip_address = '8.8.8.8'  

# Path to the GeoIP2 database file
database_path = './db/GeoLite2-City.mmdb'

# Initialize a reader object
reader = geoip2.database.Reader(database_path)

try:
    # Perform the lookup
    response = reader.city(ip_address)
    # Print all available information
    print('Country Name:', response.country.name)
    print('Country ISO Code:', response.country.iso_code)
    print('Region:', response.subdivisions.most_specific.name)
    print('City:', response.city.name)
    print('Latitude:', response.location.latitude)
    print('Longitude:', response.location.longitude)
    print('Postal Code:', response.postal.code)
    print('Time Zone:', response.location.time_zone)

except geoip2.errors.AddressNotFoundError:
    print('Address not found in the database')
finally:
    # Close the reader
    reader.close()


# Path to the GeoLite2-Country.mmdb database file
database_path = './db/GeoLite2-Country.mmdb'

# Initialize a reader object
reader = geoip2.database.Reader(database_path)

try:
    # Perform the lookup
    response = reader.country(ip_address)

    # Print the results
    print('Country Name:', response.country.name)
    print('ISO Code:', response.country.iso_code)
except geoip2.errors.AddressNotFoundError:
    print('Address not found in the database')
finally:
    # Close the reader
    reader.close()



# Path to the GeoLite2-ASN.mmdb database file
database_path = './db/GeoLite2-ASN.mmdb'

# Initialize a reader object
reader = geoip2.database.Reader(database_path)



try:
    # Perform the lookup
    response = reader.asn(ip_address)

    # Print the results
    print('ASN:', response.autonomous_system_number)
    print('ASN Organization:', response.autonomous_system_organization)
except geoip2.errors.AddressNotFoundError:
    print('Address not found in the database')
finally:
    # Close the reader
    reader.close()








    # asn_response = reader.asn(ip_address)
# print('ASN:', asn_response.autonomous_system_number)
# print('ASN Organization:', asn_response.autonomous_system_organization)