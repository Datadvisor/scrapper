from re import findall, IGNORECASE

from src.request_handler import get_page_soup, find_elements


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

    soup = get_page_soup(url)

    if soup:
        job = find_elements(soup, 'h2',
                            "top-card-layout__headline break-words font-sans text-md leading-open text-color-text")

        if job is not None:
            data.append(format_text(job))

    return ' '.join(data)
