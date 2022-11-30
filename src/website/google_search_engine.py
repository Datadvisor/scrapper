"""
    Author: Brice Toffolon
    Create on : 08/12/2021
    About: Handle request for google search engine with a lot of different methods
"""

from bs4 import BeautifulSoup
from re import match

from src.request_handler import make_req
from src.page.page_scrapping import scrap_webpage
from src.config.social_networks import social_networks, social_networks_list, reset_social_networks


def get_url_from_a_el(element):
    start_string = 'href="'
    try:
        element = str(element)
    except Exception:
        return None
    link_loc = element.find(start_string)
    end_loc = element.find('"', link_loc + len(start_string), len(element))

    if link_loc == -1 or end_loc == -1:
        return None
    return element[link_loc + len(start_string): end_loc]


def get_google_results(html_source, username):
    reset_social_networks()
    soup = BeautifulSoup(html_source, 'html.parser')

    if soup is None:
        return None
    # with open('page_source_%s.html' % username, "w") as file:
    #     file.write(html_source)
    #     file.close()
    for div in soup.findAll("div", class_="g"):
        for div_el in div.findAll("div"):
            if username.lower() in str(div_el).lower():
                for a in div_el.findAll("a", href=True):
                    url = get_url_from_a_el(a)
                    if 'translate' not in url:
                        scrap_webpage(url, social_networks_list)

    rest_of_list = [
        {
            'name': social_network,
            'link': None,
            'found': False,
            'metadata': None
        } for social_network in social_networks_list if
        sum([1 for el in social_networks['SocialNetworks'] if el['name'] == social_network]) != 1
    ]

    social_networks['SocialNetworks'] = social_networks['SocialNetworks'] + rest_of_list

    return social_networks


def sanity_check_query(query):
    if query == '':
        return {'Error': "Can't perform request for this query: %s" % query}

    if query.isdigit():
        return {'Error': "Cant perform request with digit query: %s" % query}

    if match(r'^[_\W]+$', query):
        return {'Error': "Can't perform request with only symbols: %s" % query}

    return None


def parse_results_for_demo(results):
    demo_data = False

    for website in results['SocialNetworks']:
        if website['found'] is True and demo_data is False:
            demo_data = True
            continue

        for element in website:
            if element != "found":
                website[element] = '*******' if element != "metadata" else [{"name": "*******", "value": "*******"}]

    return results


def search_in_google(query, demo):
    result = sanity_check_query(query)

    if result is not None:
        return result

    resp = make_req("https://www.google.com/search?&q=`%s`" % query)

    if resp is None:
        return {'Error': "Invalid Server Response"}

    results = get_google_results(resp['text'], query)

    if not demo:
        return results
    return parse_results_for_demo(results)
