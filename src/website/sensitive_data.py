#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 05/12/2022
    About: 

"""

from bs4 import BeautifulSoup
from re import findall

from src.request_handler import get_page_soup

from src.cv.read import find_cities, find_emails, find_urls, find_phones, find_addresses


def get_element_about_user(content, username):
    occurrences = findall('(?:[A-Za-zÀ-ú' + "'" + f'&\-," ]+ |){username.lower()}[A-Za-zÀ-ú' + "'" + ')," ]+(?:.|<)', content.lower())

    return occurrences


def get_sensitive_data(url, username):
    soup = get_page_soup(url)

    if soup:
        content = soup.text

        results = [
            {'name': 'about', 'value': ' '.join(get_element_about_user(content, username))},
            {'name': 'emails', 'value': ' '.join(find_emails(content))},
            {'name': 'cities', 'value': ' '.join(find_cities(content))},
            {'name': 'addresses', 'value': ' '.join(find_addresses(content))},
            {'name': 'phones', 'value': ' '.join(find_phones(content))},
            {'name': 'urls', 'value': ' '.join(find_urls(content))}
        ]

        return [element for element in results if element['value'] != '']

    return None

