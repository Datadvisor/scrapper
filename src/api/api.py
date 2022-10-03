#!/usr/bin/env python3

"""
    Author: bricetoffolon
    Created on: 01/06/2022
    About: API handling with FASTAPI
"""

import os
import shutil

from datetime import datetime

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.cv.read import read_cv
from src.website.google_search_engine import search_in_google
from src.mail_request import search_mail
from src.request_handler import response_format

from src.face_recognition.face_processing import faces_compare

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


@app.post("/cv/upload")
async def create_upload_file(upload_file: UploadFile):
    print(upload_file.filename)

    try:
        with open("data/" + upload_file.filename, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

    start_time = datetime.now()
    res = read_cv("data/" + upload_file.filename)

    print("Executed in: ", datetime.now() - start_time)
    os.remove("data/" + upload_file.filename)
    return res


@app.post("/search_face_recognition")
async def search_by_face(upload_file: UploadFile, query: str):
    fp = f'data/{upload_file.filename}'

    dir_name = f'data/{query.replace(" ", "")}'

    if not upload_file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file have been provided"
        )

    try:
        with open(fp, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.file.close()

    res = faces_compare(dir_name, fp, query)

    if type(res) is str:
        HTTPException(
            400,
            detail={"data": res}
        )

    os.remove(fp)

    return res




