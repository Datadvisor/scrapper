#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 06/12/2022
    About:

"""

from os import environ

from dotenv import dotenv_values


def connect_selenium_to_a_proxy(webdriver):
    try:
        proxy_address = dotenv_values()['PROXY_ADDRESS']
    except KeyError:
        proxy_address = environ['PROXY_ADDRESS']

    if not proxy_address or proxy_address.lower() == "none" or proxy_address.lower() == "null":
        return webdriver

    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": proxy_address,
        "sslProxy": proxy_address,
        "proxyType": "MANUAL",
    }

    return webdriver