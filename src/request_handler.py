"""
    Author: Brice Toffolon
    Created on : 08/12/2021
    About: To handle any request
"""
import random

import requests as req

from time import sleep

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.config.user_agent import userAgent
from src.proxy_handler import connect_selenium_to_a_proxy


def find_elements(soup, tag: str, class_name: str) -> list:
    elements = soup.findAll(tag, {"class": class_name})

    if not elements:
        return None

    return elements


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


def firefox_webdriver(use_proxy=False, headless=True) -> webdriver:
    custom_webdriver = webdriver

    if use_proxy:
        custom_webdriver = connect_selenium_to_a_proxy(webdriver)

    options = Options()

    options.headless = headless

    return custom_webdriver.Firefox(options=options)


def get_page_soup(url, use_proxy=True, headless=True):
    try:
        driver = firefox_webdriver(use_proxy=use_proxy, headless=headless)

        #driver.get('https://whatismyipaddress.com')
        driver.get(url)

        sleep(10)
        page_source = driver.page_source
    finally:
        if driver:
            driver.quit()

    if page_source:
        return BeautifulSoup(page_source, "html.parser")

    return None


def response_format(response):
    if 'Error' in response:
        raise HTTPException(
            status_code=400,
            detail=response['Error']
        )

    return JSONResponse(content=response)
