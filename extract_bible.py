import pandas as pd 
from bs4 import BeautifulSoup
import requests
import re
import json

def get_html(url):
    r = requests.get(url)
    return r.text

def clean_mye(lst):
    lst=[x.get_text() for x in lst if not re.match(r"\d+",x.get_text())]
    return [x for x in lst if not re.match(r"\s+",x)]

def clean_fr(lst):
    lst = [x.get_text() for x in list(lst)]
    lst.remove(' ')
    lst = list(map(lambda x:"" if x=="#" else x,lst))
    lst = re.split(r'\d+',''.join(lst))
    return lst.remove('')

data = {'Myènè':[],'Français':[]}

"""
Requête
GET:https://www.bible.com/api/bible/version/3438
"""
with open ('response.json',encoding='utf-8') as f:
    response = json.loads(f.read())
    
for x in response['books']:
    for y in x['chapters']:
        url = f"https://www.bible.com/bible/3438/{y['usfm']}.MYE?parallel=93"
        soup = BeautifulSoup(get_html(url),'html.parser')
        
        #Séparer la partie fr/mye
        mye= soup.find(lang="mye")
        fr=soup.find(lang="fr")

        #Extraire versets Gabonais
        m_verses = mye.find_all('span')
        m_verses = clean_mye(list(m_verses))

        #Extraire les versets Français
        f_verses = fr.find_all('span',{'class':['ChapterContent_content__RrUqA','ChapterContent_label__R2PLt']})# ou ('span',class_= False)
        f_verses = [x.get_text() for x in list(f_verses)]
        f_verses.remove(' ')
        f_verses = list(map(lambda x:"" if x=="#" else x,f_verses))
        f_verses = re.split(r'\d+',''.join(f_verses))
        f_verses.remove('')

        print((len(m_verses),len(f_verses))) #/!\ CHECK POINT
        
        if len(m_verses) == len(f_verses):
            results = list(zip(m_verses,f_verses))
            data['Myènè'].extend(m_verses)
            data['Français'].extend(f_verses)

df = pd.DataFrame.from_dict(data)
df.to_csv('resultats.csv')
print(df)

