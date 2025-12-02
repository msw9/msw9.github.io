import pandas as pd 
from bs4 import BeautifulSoup
import requests
import os
import re
import pickle


url = "https://www.bible.com/bible/3438/GEN.1.MYE?parallel=93"

def get_html(url):
    r = requests.get(url)
    return r.text

def clean_mye(lst):
    lst=[x.get_text() for x in lst if not re.match(r"\d+",x.get_text())]
    return [x for x in lst if not re.match(r"\s+",x)]

if os.path.isfile("bible.pkl"):
    with open ("bible.pkl","rb") as f:
        soup = pickle.load(f)
else:            
    soup = BeautifulSoup(get_html(url),'html.parser')
    with open ("bible.pkl","wb") as f:
        pickle.dump(soup,f)

#Séparer la partie fr/mye
mye= soup.find(lang="mye")
fr=soup.find(lang="fr")

#Extraire versets Gabonais
m_verses = mye.find_all('span')
m_verses = clean_mye(list(m_verses))

#Extraire les versets Français
f_verses = fr.find_all('span',{'class':['ChapterContent_content__RrUqA','ChapterContent_label__R2PLt']}) # ou ('span',class_= False)
f_verses = [x.get_text() for x in list(f_verses)]
f_verses.remove(' ')
f_verses = list(map(lambda x:"" if x=="#" else x,f_verses))
f_verses = re.split(r'\d+',''.join(f_verses))
f_verses.remove('')

print((len(m_verses),len(f_verses))) #/!\ CHECK POINT

results = list(zip(m_verses,f_verses))

df = pd.DataFrame(results, columns = ['Myènè', 'Français'])

df.to_csv('resultats.csv')
print(df)
