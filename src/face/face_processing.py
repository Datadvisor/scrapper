#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 29/09/2022
    About:

"""

from os import listdir, path, remove, environ

from shutil import rmtree

from time import sleep

from PIL import Image
from PIL.ExifTags import TAGS

from fastapi.responses import JSONResponse

import urllib

import face_recognition
import cv2

from dotenv import dotenv_values

from website.google_image_download import search_google_image


def get_metadata(images_to_compare: dict, dir_name: str, img_id: str) -> None:
    images_to_compare[img_id]['metadata'] = {}

    if not path.isfile(f"{dir_name}/{img_id}_validate.jpeg"):
        return None

    img = Image.open(f"{dir_name}/{img_id}_validate.jpeg")

    exifdata = img.getexif()

    for tagid in exifdata:
        images_to_compare[img_id]['metadata'][TAGS.get(tagid, tagid)] = str(exifdata.get(tagid))


def load_user_agent(user_agent):
    opener = urllib.request.build_opener()

    opener.addheaders = [('User-Agent', user_agent)]

    urllib.request.install_opener(opener)


def faces_compare(dir_name: str, face_path: str, query) -> dict:
    config = dotenv_values('.env') if dotenv_values('.env') else environ

    load_user_agent(config['USER_AGENT'])

    if not face_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return "Provide a image with a correct format: PNG, JPG OR JPEG"

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

            if results and results[0]:
                try:
                    urllib.request.urlretrieve(images_to_compare[img_id]['src'], f"{dir_name}/{img_id}_validate.jpeg")
                except (urllib.error.URLError, urllib.error.ContentTooShortError):
                    pass

                get_metadata(images_to_compare, dir_name, img_id)
                matched_face.append(images_to_compare[img_id])

    rmtree(dir_name)

    return JSONResponse(content={'data': matched_face})
