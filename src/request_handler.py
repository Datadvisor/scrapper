"""
    Author: Brice Toffolon
    Created on : 08/12/2021
    About: To handle any request
"""
import random

from fastapi import HTTPException
from fastapi.responses import JSONResponse

import requests as req
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from src.config.user_agent import userAgent


def make_req(link):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'www.google.com',
        'User-Agent': random.choice(userAgent),
        'Accept-Language': 'en-GB,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    try:
        resp = req.get(link, headers=headers)
    except Exception:
        return None

    if resp.status_code != 200:
        return None
    return {'code': resp.status_code, 'text': resp.text}


def make_sel_req(link):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    if driver is None:
        return None
    driver.get(link)
    return driver


def response_format(response):
    if 'Error' in response:
        raise HTTPException(
            status_code=400,
            detail=response['Error']
        )

    return JSONResponse(content=response)
