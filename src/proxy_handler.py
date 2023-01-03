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
    proxy_address = None

    try:
        proxy_address = dotenv_values()['PROXY_ADDRESS']
    except KeyError:
        pass

    try:
        proxy_address = environ['PROXY_ADDRESS']
    except KeyError:
        pass

    if not proxy_address:
        return webdriver

    webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        "httpProxy": proxy_address,
        "sslProxy": proxy_address,
        "proxyType": "MANUAL",
    }

    return webdriver