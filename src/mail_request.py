#!/usr/bin/env python3

"""
        backend

    Author: bricetoffolon
    Created on: 01/06/2022
    About: Making breachdirectory.org API call to search mail leak

"""

import requests

from os import environ

from dotenv import dotenv_values


def sanity_check_query(query):
    if query == '':
        return {'Error': "Can't perform request for this query: %s" % query}

    if '@' not in query and '.' not in query:
        return {'Error': "Can't perform request for this query: %s - invalid mail" % query}

    return None


def search_mail(query: str) -> dict:
    result = sanity_check_query(query)

    url: str = "https://breachdirectory.p.rapidapi.com/"

    querystring: dict = {"func": "auto", "term": query}

    config = dotenv_values('.env')

    if not config:
        config = environ

    headers: dict = {
        "X-RapidAPI-Host": config['BREACHDIRECTORY_RAPID_API_HOST'],
        "X-RapidAPI-Key": config["BREACHDIRECTORY_RAPID_API_KEY"]
    }

    if result is not None:
        return result

    response: requests.request = requests.request("GET", url, headers=headers, params=querystring)

    if not 200 <= response.status_code <= 209:
        return {
            "success": False,
        }

    if '"success": true' not in response.text:
        return {
            "success": True,
            "found": 0,
            "result": []
        }

    return response.json()
