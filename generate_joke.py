import requests

def get_joke():
    url = "https://icanhazdadjoke.com/"
    response = requests.get(url, headers = {'Accept' : 'application/json'})
    raw_joke = response.json()
    joke = raw_joke['joke']
    return joke
