import sys
import requests
from bs4 import BeautifulSoup, NavigableString

# globals
medium_search = 'https://medium.com/search?q='
medium_top = 'https://medium.com/browse/top'

def medium_urls(event, context):
    search_term = event.get("search_term", None)
    if search_term:
        page = requests.get(medium_search + search_term).content
        soup_page = BeautifulSoup(page, 'html.parser')
    else:
        page = requests.get(medium_top).content
        soup_page = BeautifulSoup(page, 'html.parser')
    titles = soup_page.find_all(['h2', 'h3'], {'class': lambda x: 'graf--title' in x.split()})
    links = soup_page.find_all('a', {'data-action': 'open-post'})
    links_and_titles = zip(titles, links)
    return [(title.string.encode('ascii', 'ignore'), link['data-action-value']) for (title, link) in links_and_titles]
