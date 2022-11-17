#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 07/11/2022
    About: 

"""


from time import sleep

from re import findall, IGNORECASE

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def find_elements(soup, tag: str, class_name: str) -> list:
    elements = soup.findAll(tag, {"class": class_name})

    if not elements:
        return None

    return elements


def twitter_scrap_profile(url):
    data = []

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    driver.get(url)

    sleep(10)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    driver.close()

    if page_source:
        profil = find_elements(soup, 'div', 'css-1dbjc4n r-1ifxtd0 r-ymttw5 r-ttdzmv')

        if profil:
            profil_description = find_elements(profil[0], 'span', "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")

            return ' '.join(element.text for element in profil_description)

    return None


if __name__ == "__main__":
    twitter_scrap_profile("https://twitter.com/anthoni_marie")
