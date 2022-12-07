#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 07/11/2022
    About: 

"""

from src.request_handler import get_page_soup, find_elements


def twitter_scrap_profile(url):
    soup = get_page_soup(url)

    if soup:
        profil = find_elements(soup, 'div', 'css-1dbjc4n r-1ifxtd0 r-ymttw5 r-ttdzmv')

        if profil:
            profil_description = find_elements(profil[0], 'span', "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0")

            if profil_description:
                return ' '.join(element.text for element in profil_description)

    return None


if __name__ == "__main__":
    twitter_scrap_profile("https://twitter.com/anthoni_marie")
