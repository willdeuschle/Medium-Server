import requests
import unidecode
import simplejson
from pattern.web import plaintext
from bs4 import BeautifulSoup, NavigableString


def medium_page(event, context):
    url = event.get('url', None)
    page = requests.get(url).content
    soup_page = BeautifulSoup(page, 'html.parser')
    content = soup_page.find('div', class_='section-content')
    str_content = str(content)
    plain_content = plaintext(str_content)
    decoded_content = unidecode.unidecode(plain_content)
    return simplejson.dumps(decoded_content.replace('\n', ' '))
