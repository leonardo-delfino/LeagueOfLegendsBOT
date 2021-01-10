import json
import urllib.request
from bs4 import BeautifulSoup


def get_json_link():
    html_page = urllib.request.urlopen("https://developer.riotgames.com/docs/lol")
    soup = BeautifulSoup(html_page, "html.parser")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))

    for link in links:
        if link is not None and "champion.json" in link:
            return link


def create_champions_hashmap():
    with urllib.request.urlopen(get_json_link()) as url:
        data = json.loads(url.read().decode())

    keys = []
    for key in data['data']:
        keys.append(key)

    values = []
    for name in keys:
        values.append(data['data'][name]['key'])

    return dict(zip(keys, values))
