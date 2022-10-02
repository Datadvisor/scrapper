#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 29/09/2022
    About: 

"""

from os import listdir, path, remove

from shutil import rmtree

from time import sleep

from PIL import Image
from PIL.ExifTags import TAGS

from fastapi.responses import JSONResponse

from urllib.request import urlretrieve

import face_recognition
import cv2

from src.website.google_image_download import search_google_image


def get_metadata(images_to_compare: dict, dir_name: str, img_id: str) -> None:
    img = Image.open(f"{dir_name}/{img_id}_validate.jpeg")

    exifdata = img.getexif()

    images_to_compare[img_id]['metadata'] = {}

    for tagid in exifdata:
        images_to_compare[img_id]['metadata'][TAGS.get(tagid, tagid)] = str(exifdata.get(tagid))


def faces_compare(dir_name: str, face_path: str, query) -> dict:
    my_face = face_recognition.load_image_file(face_path)

    if not face_recognition.face_locations(my_face):
        remove(face_path)
        return "Provide an another image, don't able to detect a face"

    my_face_encoding = face_recognition.face_encodings(my_face)[0]

    images_to_compare = search_google_image(dir_name, query)

    matched_face: list = []

    if not path.isdir(dir_name):
        return "This is bad :("

    for img in listdir(dir_name):
        img_path = f'{dir_name}/{img}'
        img_to_compare = face_recognition.load_image_file(img_path)
        img_id = img.replace('.png', '')

        faces_locations = face_recognition.face_locations(img_to_compare)

        if not faces_locations:
            continue

        for face_encoding in face_recognition.face_encodings(img_to_compare):
            results = face_recognition.compare_faces([my_face_encoding], face_encoding)

            if results[0]:
                urlretrieve(images_to_compare[img_id]['src'], f"{dir_name}/{img_id}_validate.jpeg")
                sleep(1)
                get_metadata(images_to_compare, dir_name, img_id)
                matched_face.append(images_to_compare[img_id])

    rmtree(dir_name)

    return JSONResponse(content={'data': matched_face})
