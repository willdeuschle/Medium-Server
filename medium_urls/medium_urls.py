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
        # found by inspecting the source
        piece_flag = 'postArticle postArticle--short js-postArticle js-trackedPost'
    else:
        page = requests.get(medium_top).content
        soup_page = BeautifulSoup(page, 'html.parser')
        # found by inspecting the source
        piece_flag = 'streamItem streamItem--bmPostPreview js-streamItem'
    # gets each of the articles
    pieces = soup_page.find_all('div', {'class': piece_flag})
    # going to populate these
    titles = []
    links = []
    avatars = []
    authors = []
    for piece in pieces:
        titles.append(piece.find(['h2', 'h3'], {'class': lambda x: 'graf--title' in x.split()}))
        links.append(piece.find('a', {'data-action': 'open-post'}))
        avatars.append(piece.find('img', {'class': lambda x: 'avatar-image' in x.split()}))
        for a in piece.find_all('a', {'data-action': 'show-user-card'}):
            if 'avatar' in a.get('class'):
                continue
            else:
                authors.append(a)
                break

    # occasionally there aren't titles
    coerce_to_untitled = lambda title: title.string if title else 'Untitled'

    links_titles_avatars_authors = zip(titles, links, avatars, authors)
    return [{'title': coerce_to_untitled(title), 'url': link['data-action-value'], 'avatar': avatar['src'], 'author': author.string} for (title, link, avatar, author) in links_titles_avatars_authors]
