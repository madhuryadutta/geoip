import os
import datetime
import ipaddress
import geoip2.database

# from typing import Union
# from fastapi import FastAPI, Request
from fastapi import APIRouter, Request

router = APIRouter()


# Initialize GeoIP readers
city_database_path = "./db/GeoLite2-City.mmdb"
country_database_path = "./db/GeoLite2-Country.mmdb"
asn_database_path = "./db/GeoLite2-ASN.mmdb"


def find_geo(ip_address):
    geoipdata = {}
    # Path to the GeoIP2 City ,Country,ASN database file
    city_database_path = "./db/GeoLite2-City.mmdb"
    country_database_path = "./db/GeoLite2-Country.mmdb"
    asn_database_path = "./db/GeoLite2-ASN.mmdb"

    # Initialize reader object named reader_city ,reader_country ,reader_asn
    reader_city = geoip2.database.Reader(city_database_path)
    reader_country = geoip2.database.Reader(country_database_path)
    reader_asn = geoip2.database.Reader(asn_database_path)

    try:
        # Perform the lookup
        response = reader_city.city(ip_address)
        geoipdata["ip_version"] = get_ip_version(ip_address)
        geoipdata["ip"] = ip_address
        geoipdata["country"] = response.country.name or "Unknown"
        geoipdata["iso_code"] = response.country.iso_code or "Unknown"
        geoipdata["subdivisions"] = (
            response.subdivisions.most_specific.name or "Unknown"
        )
        geoipdata["city"] = response.city.name or "Unknown"
        geoipdata["latitude"] = response.location.latitude or "Unknown"
        geoipdata["longitude"] = response.location.longitude or "Unknown"

        geoipdata["postal_code"] = response.postal.code or "Unknown"
        geoipdata["time_zone"] = response.location.time_zone or "Unknown"

    except geoip2.errors.AddressNotFoundError:
        print("Address not found in the database")
    finally:
        # Close the reader
        reader_city.close()
    try:
        # Perform the lookup
        response = reader_country.country(ip_address)
        try:
            continent_name = response.continent.names.get("en")
            geoipdata["continent_name"] = (
                continent_name if continent_name else "Unknown"
            )
        except Exception as e:
            print("Error retrieving continent name:", e)
            geoipdata["continent_name"] = "Unknown"

        try:
            continent_code = response.continent.code
            geoipdata["continent_code"] = (
                continent_code if continent_code else "Unknown"
            )
        except Exception as e:
            print("Error retrieving continent code:", e)
            geoipdata["continent_code"] = "Unknown"
    except geoip2.errors.AddressNotFoundError:
        print("Address not found in the database")
    finally:
        # Close the reader
        reader_country.close()

    try:
        # Perform the lookup
        response = reader_asn.asn(ip_address)

        geoipdata["asn"] = response.autonomous_system_number
        geoipdata["asn_org"] = response.autonomous_system_organization
    except geoip2.errors.AddressNotFoundError:
        print("Address not found in the database")
    finally:
        # Close the reader
        reader_asn.close()

    if "latitude" in geoipdata and "longitude" in geoipdata:
        geoipdata["map"] = (
            '<iframe src="https://maps.google.com/maps?q='
            + str(geoipdata["latitude"])
            + ","
            + str(geoipdata["longitude"])
            + '&hl=es;z=14&output=embed"></iframe>'
        )
    geoipdata["generatedAt"] = datetime.datetime.now()
    return geoipdata


# Helper function to check IP address validity
def is_valid_ip(ip):
    ip_address = ip.split(":")[0]
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def get_ip_version(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        if isinstance(ip, ipaddress.IPv4Address):
            return "IPv4"
        elif isinstance(ip, ipaddress.IPv6Address):
            return "IPv6"
    except ValueError:
        return "Invalid IP Address"


@router.get("/ip")
async def read_client_ip(request: Request):
    ip_address = request.client.host  # Default to the client's host IP
    cf_ip_address = request.headers.get("CF-Connecting-IP")  # Cloudflare IP
    if cf_ip_address:
        ip_address = cf_ip_address
    return {"your_ip": ip_address}


@router.get("/ip/full")
async def read_client_ip_full(request: Request):
    ip_address = request.client.host  # Default to the client's host IP
    cf_ip_address = request.headers.get("CF-Connecting-IP")  # Cloudflare IP
    if cf_ip_address:
        ip_address = cf_ip_address
    if is_valid_ip(ip_address):
        geoip_data = find_geo(ip_address)
        if geoip_data:
            return geoip_data
        else:
            return {"error": "Address not found in the database"}
    else:
        return {"error": "Invalid IP address"}


@router.get("/ip/{input_ip_address}")
async def read_item(input_ip_address: str):
    if is_valid_ip(input_ip_address):
        geoip_data = find_geo(input_ip_address)
        if geoip_data:
            return geoip_data
        else:
            return {"error": "Address not found in the database"}
    else:
        return {"error": "Invalid IP address"}
