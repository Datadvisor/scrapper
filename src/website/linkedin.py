from re import findall, IGNORECASE

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def find_elements(soup, tag: str, class_name: str) -> list:
    elements = soup.findAll(tag, {"class": class_name})

    if not elements:
        return None

    return elements


def fix_syntax(element):
    element = element.text

    words = findall("[A-zÀ-ÿ]+", element, flags=IGNORECASE)

    if not words:
        return element

    return ' '.join(words)


def format_text(elements: list):
    if len(elements) > 1:
        result = []

        for element in elements:
            result.append(fix_syntax(element))

        return result

    return fix_syntax(elements[0])


def linkedin_scrapper(url):
    data = []

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)

    driver.get(url)
    page_source = driver.page_source

    if page_source:
        soup = BeautifulSoup(page_source, "html.parser")

        job = find_elements(soup, 'h2',
                            "top-card-layout__headline break-words font-sans text-md leading-open text-color-text")

        if job is not None:
            data.append(format_text(job))

    return data