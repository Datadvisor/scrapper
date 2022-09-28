#!/usr/bin/env python3

"""
    Author: bricetoffolon
    Created on: 01/06/2022
    About: API handling with FASTAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.website.google_search_engine import search_in_google
from src.mail_request import search_mail
from src.request_handler import response_format

app = FastAPI()

origins = [
    "http://domainname.com",
    "https://domainname.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search_by_name")
async def search_by_name(query: str):
    response = search_in_google(query)

    return response_format(response)


@app.get("/search_by_mail")
async def search_by_mail(query: str):
    response = search_mail(query)

    return response_format(response)
