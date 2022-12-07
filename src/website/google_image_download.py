#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 29/09/2022
    About: Download wanted image

"""

from time import sleep
from os import mkdir, path, remove

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.request_handler import firefox_webdriver


def get_attributes(driver, locator, locator_path, attribute: str) -> str:
    try:
        web_element = driver.find_element(locator, locator_path)
    except NoSuchElementException:
        return None

    return web_element.get_attribute(attribute)


def search_google_image(dir_name: str, query: str) -> dict:
    images_to_compare: dict = {}

    try:
        driver = firefox_webdriver(headless=False)

        driver.get(f'https://www.google.ca/imghp?q={query}')
        driver.find_element(By.CSS_SELECTOR, "#L2AGLb > div").click()

        driver.find_element(By.CSS_SELECTOR,
                            "body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.RNNXgb > button > div > span > svg").click()

        if not path.isdir(dir_name):
            mkdir(dir_name)

        for i in range(1, 50):
            try:
                img_element = driver.find_element(By.XPATH, f"//*[@id='islrg']/div[1]/div[{i}]/a[1]")
            except NoSuchElementException:
                continue

            img_element.screenshot(f'{dir_name}/{i}.png')
            img_element.click()

            sleep(0.4)

            img_href = get_attributes(driver, By.XPATH,
                                      '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[3]/div[1]/a[1]',
                                      'href')

            img_src = get_attributes(driver, By.XPATH,
                                     '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img',
                                     'src')

            if img_src and 'data:image/' in img_src:
                driver.refresh()
                sleep(1)
                img_src = get_attributes(driver, By.XPATH,
                                         '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img',
                                         'src')

            if img_href is None or img_src is None:
                remove(f'{dir_name}/{i}.png')
                continue

            images_to_compare[f'{i}'] = ({'src': img_src, 'href': img_href})
    finally:
        if driver:
            driver.quit()

    return images_to_compare


if __name__ == "__main__":
    search_google_image('image_search/bricetoffolon', "brice toffolon")
