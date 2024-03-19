# IP Geo Location API
#### Project Initiated on 28/12/2023

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

This project is a FastAPI application designed to provide information about IP addresses, including their geographical locations. It utilizes MaxMind's GeoIP2 database for accurate location data retrieval. The application offers several endpoints which you can read about in the [documentation section](#documentation).

The project aims to offer a simple yet effective way to gather information about IP addresses programmatically. Feel free to explore!



### Build Using

- **[FastAPI](https://fastapi.tiangolo.com/)**
- **[MaxMind’s GeoIP2 databases](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)**




### How to Use:

```
pip install -r requirements.txt
uvicorn app.main:app --proxy-headers --reload 
```

## Docker (Deploy)
```
docker build -t geo-ip .
docker run -d --name geo-ip -p 80:80 geo-ip
```

API Documentation
========================================

### Base URL

`example.com`  
  

### Endpoints

#### 1\. Lookup Geographical Information by IP Address

**URL:**

    /ip/{input_ip_address}

**Method:**

    GET

**Description:**

Retrieves geographical information associated with the provided IP address.

**Parameters:**

    input_ip_address (string): The IP address to lookup.

**Response:**

    { "ipData": { ... }, "generatedAt": "datetime", "version": "string", "release_date": "string" }

#### 2\. Retrieve Client IP Address

**URL:**

    /ip/i

**Method:**

    GET

**Description:**

Retrieves the client's IP address.

**Response:**

    { "your_ip": "string" }

#### 3\. Retrieve Client IP Address with Geographical Information

**URL:**

    /ip/full

**Method:**

    GET

**Description:**

Retrieves the client's IP address along with associated geographical information.

**Response:**

    { "ipData": { ... }, "generatedAt": "datetime", "version": "string", "release_date": "string" }

#### 4\. Retrieve System Health Information

**URL:**

    /health

**Method:**

    GET

**Description:**

Retrieves system health information including CPU and RAM usage.

**Response:**

    { "CPU_usage": float, "RAM_usage": float, "generatedAt": "datetime" }

Errors
------

*   **400 Bad Request:** If the provided IP address is invalid.
*   **404 Not Found:** If the IP address is not found in the database.

Notes
-----

*   This API uses MAXMIND GeoLite2 databases for IP geolocation. Ensure that these databases are properly configured and up-to-date for accurate results.
*   Some endpoints may provide additional information such as CPU and RAM usage, version, and release date.