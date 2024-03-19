import os
import datetime
import ipaddress
import geoip2.database

from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.cpu_memory_usage import cpu_usage, memory_usage

app = FastAPI()

# Mount static files directory
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return geoipdata


# Helper function to check IP address validity
def is_valid_ip(ip):
    ip_address = ip.split(":")[0]
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# Main endpoints
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def read_system_health():
    return {
        "CPU_usage": cpu_usage(),
        "RAM_usage": memory_usage(),
        "generatedAt": datetime.datetime.now(),
    }


@app.get("/ip/i")
def read_client_ip(request: Request):
    ip_address = request.client.host  # Default to the client's host IP
    cf_ip_address = request.headers.get("CF-Connecting-IP")  # Cloudflare IP
    if cf_ip_address:
        ip_address = cf_ip_address
    return {"your_ip": ip_address}


@app.get("/ip/full")
def read_client_ip_full(request: Request):
    ip_address = request.client.host  # Default to the client's host IP
    cf_ip_address = request.headers.get("CF-Connecting-IP")  # Cloudflare IP
    if cf_ip_address:
        ip_address = cf_ip_address
    if is_valid_ip(ip_address):
        geoip_data = find_geo(ip_address)
        if geoip_data:
            return {
                "ipData": geoip_data,
                "generatedAt": datetime.datetime.now(),
            }
        else:
            return {"error": "Address not found in the database"}
    else:
        return {"error": "Invalid IP address"}


@app.get("/ip/{input_ip_address}")
def read_item(input_ip_address: str):
    if is_valid_ip(input_ip_address):
        geoip_data = find_geo(input_ip_address)
        if geoip_data:
            return {
                "ipData": geoip_data,
                "generatedAt": datetime.datetime.now(),
            }
        else:
            return {"error": "Address not found in the database"}
    else:
        return {"error": "Invalid IP address"}
