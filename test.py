import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_duckduckgo(query):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        res = requests.post(url, headers=headers, data={'q': query})
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', class_='result__snippet'):
            print(a.text)
    except Exception as e:
        print(e)

search_duckduckgo('\"cameron snider\" \"richmond\" \"michigan\" linkedin')
