#!/usr/bin/env python3

"""
        backend

    Author: bricetoffolon
    Created on: 01/06/2022
    About: Making breachdirectory.org API call to search mail leak

"""

import requests

from re import match


def sanity_check_query(query):
    if query == '':
        return {'Error': "Can't perform request for this query: %s" % query}

    if '@' not in query and '.' not in query:
        return {'Error': "Can't perform request for this query: %s - invalid mail" % query}

    return None


def search_mail(query: str) -> str:
    result = sanity_check_query(query)

    url: str = "https://breachdirectory.p.rapidapi.com/"

    querystring: dict = {"func": "auto", "term": query}

    headers: dict = {
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com",
        "X-RapidAPI-Key": "38b4e8bfb6mshec6dc4ce99efd1ap121365jsn7c75210f493f"
    }

    if result is not None:
        return result

    response: requests.request = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()
