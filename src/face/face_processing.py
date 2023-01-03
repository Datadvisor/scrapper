#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 29/09/2022
    About:

"""

from os import listdir, path, remove, environ

from shutil import rmtree

from PIL import Image
from PIL.ExifTags import TAGS

from fastapi.responses import JSONResponse

import face_recognition

from dotenv import dotenv_values

from src.website.google_image_download import search_google_image


def get_metadata(images_to_compare: dict, dir_name: str, img_id: str, fp: str) -> None:
    images_to_compare[img_id]['metadata'] = {}

    img = Image.open(fp)

    exifdata = img.getexif()

    for tagid in exifdata:
        images_to_compare[img_id]['metadata'][TAGS.get(tagid, tagid)] = str(exifdata.get(tagid))


def faces_compare(dir_name: str, face_path: str, query) -> dict:
    try:
        config = dotenv_values('.env')
    except Exception:
        config = environ

    if 'GOOGLE_CUSTOM_SEARCH_API_KEY' not in config:
        return []

    api_key = config['GOOGLE_CUSTOM_SEARCH_API_KEY']

    if not face_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return "Provide a image with a correct format: PNG, JPG OR JPEG"

    my_face = face_recognition.load_image_file(face_path)

    if not face_recognition.face_locations(my_face):
        remove(face_path)
        return "Provide an another image, don't able to detect a face"

    my_face_encoding = face_recognition.face_encodings(my_face)[0]

    images_to_compare = search_google_image(dir_name, query, api_key)

    matched_face: list = []

    if not path.isdir(dir_name):
        return "This is bad :("

    for img in listdir(dir_name):
        if '.jpg' not in img and '.png' not in img:
            continue

        img_path = f'{dir_name}/{img}'

        img_to_compare = face_recognition.load_image_file(img_path)
        img_id = img.split('.')[0]

        faces_locations = face_recognition.face_locations(img_to_compare)

        if not faces_locations:
            continue

        for face_encoding in face_recognition.face_encodings(img_to_compare):
            results = face_recognition.compare_faces([my_face_encoding], face_encoding)

            if results and results[0]:
                get_metadata(images_to_compare, dir_name, img_id, img_path)
                matched_face.append(images_to_compare[img_id])

    rmtree(dir_name)

    return JSONResponse(content={'data': matched_face})
