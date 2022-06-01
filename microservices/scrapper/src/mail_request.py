#!/usr/bin/env python3

"""
        backend

    Author: bricetoffolon
    Created on: 01/06/2022
    About: Making breachdirectory.org API call to search mail leak

"""

import requests


def search_mail(mail: str) -> str:
    url: str = "https://breachdirectory.p.rapidapi.com/"

    querystring: dict = {"func": "auto", "term": mail}

    headers: dict = {
        "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com",
        "X-RapidAPI-Key": "38b4e8bfb6mshec6dc4ce99efd1ap121365jsn7c75210f493f"
    }

    response: requests.request = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()
