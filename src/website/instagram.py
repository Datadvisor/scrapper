#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 07/11/2022
    About: 

"""

from src.request_handler import get_page_soup, find_elements


def instagram_scrap_profile(url):
    soup = get_page_soup(url, headless=True, use_proxy=True)

    if soup:
        profil_description = find_elements(soup, 'div', '_aacl _aacp _aacu _aacx _aad6 _aade')
        profil_img = find_elements(soup, 'img',
                                   'xh8yej3 x11njtxf xkhd6sd x18d9i69 x4uap5 xexx8yu x1mh8g0r xat24cr x11i5rnm xdj266r xpdipgo x5yr21d xk390pu xav7gou xaqea5y x1b1mbwd x6umtig')

        if profil_description:
            return ' '.join(element.text for element in profil_description)

    return None


if __name__ == "__main__":
    instagram_scrap_profile("https://www.instagram.com/anthoni.marie/?hl=fr")
