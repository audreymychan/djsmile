# This script contains the get_joke() function to generate a new dad joke

import requests


def get_joke():
    """Return new joke string from icanhazdadjoke.com."""
    url = "https://icanhazdadjoke.com/"
    response = requests.get(url, headers={'Accept': 'application/json'})
    raw_joke = response.json()
    joke = raw_joke['joke']
    return joke
