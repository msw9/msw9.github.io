import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

def get_html(url):
    r = requests.get(url)
    return r.text

"""
Extraire
"""
liens = ["https://web.archive.org/web/20170503165023/http://www.awanawintche.com/proverbes-omyene-chapitre-1/",
"https://web.archive.org/web/20170501231142/http://www.awanawintche.com/proverbes-omyene-chapitre-2/",
"https://web.archive.org/web/20171210000635/http://www.awanawintche.com/proverbes-omyene-chapitre-3"]

for lien in liens:
    soup = BeautifulSoup(get_html(lien),'html.parser')
    article = soup.find('div',class_='entry-content resize')
    proverbes = article.find_all('h2')
    print([x.get_text() for x in list(proverbes)])
