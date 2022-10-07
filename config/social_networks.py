"""
    Author: Brice Toffolon
    Created on : 14/12/2021
    About: Social network informations
"""

social_networks = \
    {
        'SocialNetworks': [],
        'Others': {
                'relatedLink': []
        }
    }

social_networks_list = ["Google", "Youtube", "Facebook", "Instagram", "Spotify", "Twitter", "Steam", "Microsoft",
                        "Linkedin"]


def reset_social_networks():
    social_networks['SocialNetworks'] = []
    social_networks['Others']["relatedLink"] = []
