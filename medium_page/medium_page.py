import requests
import unidecode
from pattern.web import plaintext
from bs4 import BeautifulSoup


def medium_page(event, context):
    url = event.get('url', None)
    page = requests.get(url).content
    soup_page = BeautifulSoup(page, 'html.parser')
    # find all the content
    content = soup_page.find_all('div', class_='section-content')
    # map over it to parse out the nonsense, convert to unicode
    content = map(lambda content_subpiece: unidecode.unidecode(plaintext(str(content_subpiece))), content)
    # join with new lines
    decoded_content = '\n\n'.join(content)
    return decoded_content
