#!/usr/bin/env python3

"""
        scrapper

    Author: bricetoffolon
    Created on: 29/09/2022
    About: Download wanted image

"""

from time import sleep
from os import mkdir, path
from traceback import format_exc

from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

import seleniumwire.undetected_chromedriver as uc


def get_attributes(driver, locator, locator_path, attribute: str) -> str:
    web_element = driver.find_element(locator, locator_path)

    if web_element:
        return web_element.get_attribute(attribute)

    return None


def create_driver() -> webdriver:
    chrome_options: uc.options.ChromeOptions = uc.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')

    return uc.Chrome(
        options=chrome_options,
        seleniumwire_options={
            'request_storage': 'memory',
            'request_storage_max_size': 1000
        }
    )


def search_google_image(dir_name: str, query: str) -> dict:
    images_to_compare: dict = {}

    driver = create_driver()

    driver.get(f'https://www.google.ca/imghp?q={query}')

    driver.find_element(By.CSS_SELECTOR, "#L2AGLb > div").click()

    driver.find_element(By.CSS_SELECTOR,
        "body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > div.A8SBwf > div.RNNXgb > button > div > span > svg").click()

    if not path.isdir(dir_name):
        mkdir(dir_name)

    for i in range(1, 100):
        try:
            img_element = driver.find_element(By.XPATH, f"//*[@id='islrg']/div[1]/div[{i}]/a[1]")

            img_element.screenshot(f'{dir_name}/{i}.png')

            img_element.click()

            sleep(0.4)

            img_href = get_attributes(driver, By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[3]/div[1]/a[1]', 'href')

            img_src = get_attributes(driver, By.XPATH, '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img', 'src')

            if 'data:image/' in img_src:
                driver.refresh()
                sleep(1)
                img_src = get_attributes(driver, By.XPATH,
                                         '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img',
                                         'src')

            images_to_compare[f'{i}'] = ({'src': img_src, 'href': img_href})

        except:
            #print(format_exc())
            break

    driver.close()

    return images_to_compare


if __name__ == "__main__":
    search_google_image('image_search/bricetoffolon',"brice toffolon")
