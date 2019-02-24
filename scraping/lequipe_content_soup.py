# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:59:35 2019

==================================L'EQUIPE=====================================

"""
# =============================================================================
#                                 Packages
# =============================================================================

from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import datetime
import json
import time
from datetime import datetime as dt2
import locale
locale.setlocale(locale.LC_TIME,'')


# =============================================================================
#                     Récupération du code source d'une page
# =============================================================================

def create_soup(url):
    
    """ 
        Prend en entrée l'url d'une page web
        Retourne son code source  
        
    """
    
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    return(soup)


# =============================================================================
#             Récupération des URLs d'une recherche sur un site web
# =============================================================================

def get_articles_urls(nb):
    
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant à la recherche 
        "coupe du monde 2022 qatar" sur le site "l'Equipe"   
        tri par pertinence
        
    """
    
    urls_list = []

    for i in range(1, nb+1):
        url_search = 'https://www.lequipe.fr/recherche/search.php?r=coupe+du+monde+2022+qatar&jd=01&md=01&ad=2019&jf=01&mf=01&af=2019&t=ALL&adv=0&o=P&s=ALL&s1=efr&p=' + str(i)
        soup = create_soup(url_search)
    
        for h2 in soup.find_all('h2'):
            for a in h2.find_all('a'):
                url = 'https://www.lequipe.fr' + a.get("href")
                urls_list.append(url)
    
    urls_list = list(set(urls_list))  
                      
    return(urls_list)


# =============================================================================
#                       Récupération du contenu des articles
# =============================================================================

def get_1_article_content(url):
    
    """ 
        Prend en entrée l'url d'un article
        Retourne : source, url, date, thème, titre, sous-titre, contenu , abo, type de contenu   
    
    """
    
    soup = create_soup(url)
    source = "lequipe"
    date, theme, title, subtitle, content, abo, content_type = "", "", "", "", "", "", "article"
   
    try:
        #date
        for div in soup.find_all('div', class_ = 'article__date'):
            date = div.find('time').get_text()
        if date.find("à") != -1:
            k = date.find("à") -1
            date = date[:k]
        s = ['1er', 'Ã©', 'Ã»', 'janvier', 'février', 'avril', 'juillet', 'septembre', 'octobre', 'novembre', 'décembre']
        t = ['1', 'é', 'û', 'janv.', 'févr.', 'avr.', 'juil.', 'sept.','oct.', 'nov.', 'déc.']
        for i in range(11):    
            date = date.replace(s[i], t[i])
        date = dt2.strptime(date, "%A %d %b %Y").strftime("%Y/%m/%d")
            
        #theme
        div = soup.find('div', class_ = 'surtitre article__surtitre')
        for span in div.find_all('span'):
            theme += span.get_text() + ', '
            
        #title
        try:
            if soup.find('h1').get('class')[2]  == 'article__titre':
                h1 = soup.find('h1')
                title = h1.strong.get_text()
            else:
                for header in soup.find_all('header', class_ = 'article__header js-article__header'):
                    title = header.find('h1', itemprop = 'headline').get_text()
        except:
            title = soup.find('h1', itemprop = 'headline').get_text()
  
        #subtitle
        if soup.find('h2', class_ = 'article__chapeau') is not None:
            subtitle = soup.find('h2', class_ = 'article__chapeau').get_text()
                        
        #content
        for p in soup.find_all('p', class_ = 'article__paragraphe article__paragraphe--last'):
            content += p.get_text()
        if content == "":
            for div in soup.find_all('div', class_ = 'col text'):
                if div.p.get('class') is None:
                    content += div.p.get_text() + " "
            if content == "":
                for p in soup.find_all('p', class_ = 'article__paragraphe'):
                    content += p.get_text() + ""
            if content == "":
                for div in soup.find_all('div', class_ = 'article__paragraphe article__paragraphe--last'):
                    for p in div.find_all('p'):
                        content += p.get_text() + ""
            if content == "":
                for div in soup.find_all('div', class_ = 'article__paragraphe'):
                    for p in div.find_all('p'):
                        content += p.get_text() + ""
        
        #abo        
        if soup.find('div', class_ = 'div-provenance') is None:
            abo = "non"
        else:
            abo = "oui"
                    
    except:
        print("Exception : " + url+ "\n")
            
    return(str(source), str(url), str(date), str(theme), str(title), str(subtitle), str(content), str(abo), str(content_type))
               

def df_articles_content(urls_list):
    
    """ 
        Prend en entrée une liste d'urls d'articles
        avec en colonnes : 
            source, url, date, thème, titre, sous-titre, contenu, abo, type de contenu  
    
    """
    
    df = pd.DataFrame(columns=['source', 'url', 'date','theme', 'title','subtitle','content', 'abo', 'content_type'])
    
    for url in urls_list:
        s, u, d, t, ti, su, c, a, ct = get_1_article_content(url)
        i = df.shape[0]
        if d != "":
            df.loc[i+1] = [s, u, d, t, ti, su, c, a, ct]

    return(df)
    
    
# =============================================================================
#                              Sauvegarde en json
# =============================================================================

def save_as_json(df, path, filename):

    """
        Prend en entrée un dataframe
        Crée un fichier json avec le contenu du dataframe
         
    """
    
    data = df.to_dict()
    
    with open('{}\\data\\{}.json'.format(path, filename), 'w') as outfile:
        outfile.write(json.dumps(data, ensure_ascii = True, indent = 4))


# =============================================================================
#                             Exécution des fonctions
# =============================================================================

if __name__ == '__main__':
    tps_s = time.perf_counter()
    
    urls_list = get_articles_urls(45) #récupération des urls des articles
    df = df_articles_content(urls_list) #récupéation du contenu des articles, stockage dans un dataframe
    
    path = os.getcwd()
    now = datetime.datetime.now().isoformat()
    filename = now[:10] + "_all_articles_lequipe"
    save_as_json(df, path, filename) #sauvegarde en json du contenu des articles
    
    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" %(tps_e-tps_s))
