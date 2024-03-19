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
app.mount("/static", StaticFiles(directory="static"), name="static")

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


def check(ip):
    # Use the ip_address function from the ipaddress module to check if the input is a valid IP address
    try:
        ipaddress.ip_address(ip)
        print("Valid IP address")
        return 1
    except ValueError:
        # If the input is not a valid IP address, catch the exception and print an error message
        print("Invalid IP address")
        return 0


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
        geoipdata["country"] = response.country.name
        geoipdata["iso_code"] = response.country.iso_code
        geoipdata["subdivisions"] = response.subdivisions.most_specific.name
        geoipdata["city"] = response.city.name
        geoipdata["latitude"] = response.location.latitude
        geoipdata["longitude"] = response.location.longitude
        geoipdata["postal_code"] = response.postal.code
        geoipdata["time_zone"] = response.location.time_zone

    except geoip2.errors.AddressNotFoundError:
        print("Address not found in the database")
    finally:
        # Close the reader
        reader_city.close()
    try:
        # Perform the lookup
        response = reader_country.country(ip_address)

        geoipdata["continent_code"] = response.continent.code
        geoipdata["continent_name"] = response.continent.names["en"]
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


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def read_system_health():
    x = cpu_usage()
    y = memory_usage()
    return {"CPU_usage": x, "RAM_usage": y, "generatedAt": datetime.datetime.now()}


@app.get("/ip/{input_ip_address}")
def read_item(
    input_ip_address: str,
):
    x = check(input_ip_address)
    if x == 1:
        geoipData = find_geo(input_ip_address)
    else:
        geoipData = "Invalid Ip address"

    return {
        "ipData": geoipData,
        "generatedAt": datetime.datetime.now(),
        "version": "0.0.1",
        "release_date": "03/03/2024",
    }


@app.get("/ip/i")
def read_client_ip(request: Request):
    ip_address = request.client.host  # Default to the client's host IP
    # Extracting IP address and country from Cloudflare headers if present
    cf_ip_address = request.headers.get("CF-Connecting-IP")
    if cf_ip_address:
        ip_address = cf_ip_address
    return {"your_ip": ip_address}


@app.get("/ip/full")
def read_client_ip_full(request: Request):
    ip_address = request.client.host  # Default to the client's host IP
    # Extracting IP address and country from Cloudflare headers if present
    cf_ip_address = request.headers.get("CF-Connecting-IP")
    if cf_ip_address:
        ip_address = cf_ip_address

    x = check(ip_address)
    if x == 1:
        geoipData = find_geo(ip_address)
    else:
        geoipData = "Invalid Ip address"
    return {
        "ipData": geoipData,
        "generatedAt": datetime.datetime.now(),
        "version": "0.0.1",
        "release_date": "03/03/2024",
    }
