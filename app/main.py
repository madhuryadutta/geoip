import os
import datetime


from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI

# from .dependencies import get_query_token, get_token_header
from .routers import health, geoip

from pydantic import BaseModel

app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_query_token)])


# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files directory
# app.mount("/static", StaticFiles(directory="static"), name="static")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Main endpoints : Root
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(health.router)
app.include_router(geoip.router)
