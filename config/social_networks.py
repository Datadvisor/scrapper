"""
    Author: Brice Toffolon
    Created on : 14/12/2021
    About: Social network informations
"""

social_networks = \
    {
        'socialNetwork': {
            'Google': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Youtube': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Facebook': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Instagram': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Spotify': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Twitter': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Steam': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Microsoft': {
                'link': None,
                'find': False,
                'description': None,
            },
            'Linkedin': {
                'link': None,
                'find': False,
                'description': None,
            },
        },
        'Others': {
                'relatedLink': []
        }
    }

social_networks_list = ["Google", "Youtube", "Facebook", "Instagram", "Spotify", "Twitter", "Steam", "Microsoft",
                        "Linkedin"]


def reset_social_networks():
    for social_network in social_networks_list:
        social_networks['socialNetwork'][social_network]['link'] = None
        social_networks['socialNetwork'][social_network]['find'] = False
        social_networks['socialNetwork'][social_network]['description'] = None
        social_networks['Others']['relatedLink'] = []
