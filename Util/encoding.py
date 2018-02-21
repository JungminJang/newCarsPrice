import urllib.request
from urllib.parse import quote

from bs4 import BeautifulSoup
# 인코딩
def urlencode(string, type):
    return urllib.parse.quote(string, encoding=type)

# 디코딩
def urldecode(string, type):
    print(urllib.parse.unquote_plus(string, encoding=type, errors='k5'))

def soup(URLlink):
    try:
        source_code_from_URL = urllib.request.urlopen(URLlink)
    except:
        return None
    else:
        return BeautifulSoup(source_code_from_URL, 'html.parser')
