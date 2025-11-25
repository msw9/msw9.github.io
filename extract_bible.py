import pandas as pd 
from bs4 import BeautifulSoup
import requests
import os
import re
try:
    os.remove("test.txt")
except:
    pass

url = "https://www.bible.com/bible/3438/GEN.1.MYE?parallel=93"

def get_html(url):
    r = requests.get(url)
    return r.text

def clean_mye(lst):
    lst=[x.get_text() for x in lst if not re.match(r"\d+",x.get_text())]
    return [x for x in lst if not re.match(r"\s+",x)]

soup = BeautifulSoup(get_html(url),'html.parser')

#Séparer la partie fr/mye
mye= soup.find(lang="mye")
fr=soup.find(lang="fr")

#Extraire versets Gabonais
m_verses = mye.find_all('span')
m_verses = clean_mye(list(m_verses))


print(m_verses)
    


