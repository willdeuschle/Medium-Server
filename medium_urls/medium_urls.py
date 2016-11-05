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
    avatars = soup_page.find_all('img', {'class': lambda x: 'avatar-image' in x.split()})
    authors = []
    for a in soup_page.find_all('a', {'data-action': 'show-user-card'}):
        if 'avatar' in a.get('class'):
            continue
        else:
            authors.append(a)

    links_titles_avatars_authors = zip(titles, links, avatars, authors)
    return [{'title': title.string, 'url': link['data-action-value'], 'avatar': avatar['src'], 'author': author.string} for (title, link, avatar, author) in links_titles_avatars_authors]
