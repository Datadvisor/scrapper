"""
    Author: Brice Toffolon
    Created on : 26/11/2022
    About : Parse scrapping results
"""

from re import findall, sub


def treat_digit_results(results, regex_exp) -> list:
    digits_results: list = findall(regex_exp, results)

    if not digits_results:
        return []

    return [{'name': element.split(' ')[1].capitalize(), 'value': element.split(' ')[0]} for element in digits_results]


def treat_description(results) -> list:
    regex_exp = '(?=[A-Z]\w+).*'

    desc_results: list = findall(regex_exp, results)

    if not desc_results:
        return []

    sub(regex_exp, '', results)

    return [{'name': 'description', 'value': desc_results[0]}]


def parse_scrapping_results(results) -> list:
    regex_exp_digit = '\d+ [A-z]+'

    if results == [] or results is None:
        return None

    digit_results: list = treat_digit_results(results, regex_exp_digit)

    sub(regex_exp_digit, '', results)

    description_results: list = treat_description(results)

    if digit_results == [] and description_results == []:
        return [{'name': 'description', 'value': results}]

    return digit_results + description_results


