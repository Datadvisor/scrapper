"""
    Author: Brice Toffolon
    Created on : 09/12/2021
    About : To scrap any page of socialNetwork
"""

from src.website.linkedin import linkedin_scrapper
from config.social_networks import social_networks


def get_siteURI_and_linkURI(url):
    start_link = url.find('https://')

    if start_link == -1:
        return None
    end_site_URI = url.find('/', start_link + len('https://'))
    if end_site_URI != -1:
        site_URI = url[start_link + len('https://'):end_site_URI]
        site_name_loc = site_URI.rfind('.')
        if site_name_loc != -1:
            site_name = site_URI[:site_name_loc].replace('www.', '')
    return {'site': site_name, 'siteURI': site_URI}


def add_other_link(url):
    url_data = get_siteURI_and_linkURI(url)

    for link in social_networks['Others']['relatedLink']:
        if link['site'] in url:
            return None
    if url_data is not None:
        social_networks['Others']['relatedLink'].append(
            {'site': url_data['site'], 'siteURI': url_data['siteURI'], 'linkURI': url, 'overall': 'Neutre',
             'type': 'Site Web'}
        )


def scrap_webpage(url, social_network_list):
    scraper_function_list = \
        {
            'Google': None,
            'Youtube': None,
            'Facebook': None,
            'Instagram': None,
            'Spotify': None,
            'Twitter': None,
            'Steam': None,
            'Microsoft': None,
            'Linkedin': linkedin_scrapper
        }

    for social_network in social_network_list:
        if social_network.lower() in url:
            if social_networks['socialNetwork'][social_network]['find'] is False:
                social_networks['socialNetwork'][social_network]['link'] = url
                social_networks['socialNetwork'][social_network]['find'] = True
                if scraper_function_list[social_network]:
                    social_networks['socialNetwork'][social_network]['description'] = scraper_function_list[
                        social_network](url)
    add_other_link(url)
