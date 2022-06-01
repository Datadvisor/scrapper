#!/usr/bin/env python3

"""
        backend

    Author: bricetoffolon
    Created on: 01/06/2022
    About: API handling with FASTAPI

"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.mail_request import search_mail

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

@app.get("/search_by_mail")
async def search_by_mail(query: str):
    return JSONResponse(content=search_mail(query))