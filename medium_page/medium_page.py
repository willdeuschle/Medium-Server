import sys
import requests
from bs4 import BeautifulSoup, NavigableString

invalid_tags = ['b', 'i', 'u', 'strong', 'p', 'em', 'a', 'span', 'img']

def clean_text(tag):
    if tag.name in invalid_tags:
        s = ""

        for c in tag.contents:
            if not isinstance(c, NavigableString):
                c = clean_text(c)
            s += unicode(c)

        tag = s

    return tag


def medium_page(event, context):
    url = event.get('url', None)
    data_arr = []
    page = requests.get(url).content
    soup_page = BeautifulSoup(page, 'html.parser')
    stuff = soup_page.find_all('p')
    for datum in stuff:
        try:
            if "card-description" in  datum.get('class', []):
                pass
            else:
                new_datum = clean_text(datum)
                new_datum_string = new_datum.encode('ascii', 'ignore')
                data_arr.append(new_datum_string)
        except Exception, e:
            print "The exception: ", e
            pass

    article_string = " ".join(data_arr)
    return(article_string)
