"""
    Author: Brice Toffolon
    Created on : 08/12/2021
    About: To handle any request
"""
import random

import requests as req
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from config.user_agent import userAgent


def make_req(link):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host': 'www.google.com',
        'User-Agent': random.choice(userAgent),
        'Accept-Language': 'en-GB,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    resp = req.get(link, headers=headers)

    if resp.status_code != 200:
        return None
    return {'code': resp.status_code, 'text': resp.text}


def make_sel_req(link):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    if driver is None:
        return None
    driver.get(link)
    return driver
