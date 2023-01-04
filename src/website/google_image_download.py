#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 29/09/2022
    About: Download wanted image

"""

from os import mkdir, path

import requests as req
import shutil
import mimetypes


def download_img(img_url: str, dir_name, idx: int) -> None:
    fp = f'{dir_name}/{idx}'

    if type(img_url) != str or 'http' not in img_url:
        return None

    resp = req.get(img_url, stream=True)

    if resp.status_code != 200:
        return None

    content_type = resp.headers['content-type']
    ext = mimetypes.guess_extension(content_type)

    if ext:
        resp.raw.decode_content = True
        with open(fp + ext, 'wb') as f:
            shutil.copyfileobj(resp.raw, f)


def search_google_image(dir_name: str, query: str, api_key: str) -> dict:
    img_to_compare: dict = {}

    if not path.isdir(dir_name):
        mkdir(dir_name)

    resp = req.get(
        f'https://www.googleapis.com/customsearch/v1?&key={api_key}&cx=c0b9244ebc3e8494c&q={query}')

    if resp.status_code != 200:
        return None

    resp = resp.json()

    if not resp or 'items' not in resp:
        return None

    for idx, item in enumerate(resp['items']):
        if 'link' in item:
            img_to_compare[str(idx)] = ({'link': item['link']})

        if 'pagemap' in item and 'metatags' in item['pagemap']:
            for element in item['pagemap']['metatags']:
                if 'og:image' in element:
                    download_img(element['og:image'], dir_name, idx)

    return img_to_compare
