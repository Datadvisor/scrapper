from os import environ

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from dotenv import dotenv_values


def get_element_by_css(driver, css_element):
    try:
        return driver.find_element(By.CSS_SELECTOR,css_element).text
    except:
        return None


def linkedin_scrapper(url):
    data_list = []

    if not dotenv_values('.env'):
        config = environ
    else:
        config = dotenv_values('.env')

    email = config['LINKEDIN_USERNAME']
    password = config['LINKEDIN_PASSWD']

    css_elements_list = \
        [
            "div.text-body-medium",
            "div.inline-show-more-text:nth-child(2)",
            "li.pv-text-details__right-panel-item:nth-child(1) > a:nth-child(1) > h2:nth-child(2) > div:nth-child(1)"
        ]

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get("https://www.linkedin.com/")
    with open('linkedin_response.html', 'w') as file:
        file.write(driver.page_source)
    driver.find_element(By.CSS_SELECTOR, '#session_key').send_keys(email)
    driver.find_element(By.CSS_SELECTOR,'#session_password').send_keys(password)
    driver.find_element(By.CLASS_NAME, "sign-in-form__submit-button").click()

    try:
        with open('linkedin_response.html_2', 'w') as file:
            file.write(driver.page_source)
    except:
        pass
    try:
        driver.get(url)
        with open('linkedin_response.html_3', 'w') as file:
            file.write(driver.page_source)
    except:
        pass

    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "global-nav")))
    driver.get(url)
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "global-nav")))
    for css_element in css_elements_list:
        resp = get_element_by_css(driver, css_element)
        if resp is not None:
            data_list.append("%s" % resp)
    print(data_list)
    return data_list

if __name__ == "__main__":
    linkedin_scrapper('https://www.linkedin.com/in/brice-toffolon/')
