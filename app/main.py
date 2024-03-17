from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import ipaddress
import geoip2.database

# from dotenv import load_dotenv

app = FastAPI()
# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# load_data()
# load_dotenv()

# CDN = os.environ["APP_URL_ENV"]

# app.mount("/static", StaticFiles(directory="local/meme"), name="static")


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
    except ValueError:
        # If the input is not a valid IP address, catch the exception and print an error message
        print("Invalid IP address")


def find_geo(ip_address):

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
    x = 89
    return x


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/v")
def read_version(request: Request):
    client_host = request.client.host
    return {"version": "0.0.1", "release_date": "03/03/2024"}


@app.get("/ip/{input_ip_address}")
def read_item(input_ip_address: str, request: Request):
    x = find_geo(input_ip_address)
    # x = check(ip)
    print(x)
    return {"version": "0.0.1", "release_date": "03/03/2024"}


@app.get("/whoami")
def read_client(request: Request):
    client_host = request.client.host
    return {"client_ip": client_host}


# @app.get("/q/{query}")
# def read_item(query: str):
#     i = 0
#     result = {}
#     for x in source_list:
#         if query in x:
#             i = i + 1
#             url_meme = "http://" + str(CDN) + "/static/" + x
#             result.update({i: url_meme})
#     if i == 0:
#         output = "No Result found"
#     else:
#         output = result
#     return {"random_meme": output}
