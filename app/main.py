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

# Initialize GeoIP readers
city_database_path = "./db/GeoLite2-City.mmdb"
country_database_path = "./db/GeoLite2-Country.mmdb"
asn_database_path = "./db/GeoLite2-ASN.mmdb"

with geoip2.database.Reader(city_database_path) as reader_city, geoip2.database.Reader(
    country_database_path
) as reader_country, geoip2.database.Reader(asn_database_path) as reader_asn:

    def find_geo(ip_address):
        try:
            response_city = reader_city.city(ip_address)
            response_country = reader_country.country(ip_address)
            response_asn = reader_asn.asn(ip_address)

            geoipdata = {
                "country": response_city.country.name,
                "iso_code": response_city.country.iso_code,
                "subdivisions": response_city.subdivisions.most_specific.name,
                "city": response_city.city.name,
                "latitude": response_city.location.latitude,
                "longitude": response_city.location.longitude,
                "postal_code": response_city.postal.code,
                "time_zone": response_city.location.time_zone,
                "continent_code": response_country.continent.code,
                "continent_name": response_country.continent.names["en"],
                "asn": response_asn.autonomous_system_number,
                "asn_org": response_asn.autonomous_system_organization,
            }
            return geoipdata
        except geoip2.errors.AddressNotFoundError:
            return None


# Helper function to check IP address validity
def is_valid_ip(ip):
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


@app.get("/ip/{input_ip_address}")
def read_item(input_ip_address: str):
    if is_valid_ip(input_ip_address):
        geoip_data = find_geo(input_ip_address)
        if geoip_data:
            return {
                "ipData": geoip_data,
                "generatedAt": datetime.datetime.now(),
                "version": "0.0.1",
                "release_date": "03/03/2024",
            }
        else:
            return {"error": "Address not found in the database"}
    else:
        return {"error": "Invalid IP address"}


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
                "version": "0.0.1",
                "release_date": "03/03/2024",
            }
        else:
            return {"error": "Address not found in the database"}
    else:
        return {"error": "Invalid IP address"}
