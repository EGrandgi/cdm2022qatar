# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 17:44:38 2019

@author: EGrandgi
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


# =============================================================================
#                     Récupération du code soyrce d'une page
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
        "coupe du monde 2022 qatar" sur le site "L'Express"   
        
    """
    
    urls_list = []

    for i in range(1, nb+1):
        url_search = 'https://www.lexpress.fr/recherche?q=coupe+du+monde+2022+qatar&p=' + str(i)
        soup = create_soup(url_search)
        for div in soup.find_all('div'):
            if (div.get("class")!=None):
                if "img_container" in div.get("class"):
                    for a in div.find_all('a'):
                        url = a.get("href")
                        urls_list.append(url)
                
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
    source = "LExpress"
    date, theme, title, subtitle, content, abo, content_type = "", "", "", "", "", "non", ""
    
    try:
        #date
        for time_ in soup.find_all('time', itemprop = ['datePublished']):
            date = time_.get_text()[9:19]

        #theme      
        for nav in soup.find_all('nav', class_ = ['breadcrumb']):
            for li in nav.find_all('li'):
                theme += li.get_text() + ","
            
        #title
        title = soup.find('h1', class_ = "title_alpha").get_text()[11:]
        
        #subtitle
        subtitle = soup.find('h2', class_ = "chapo title_gamma").get_text()[11:]
                        
        #content
        for div in soup.find_all('div', class_ = ['article_container']):
            for p in div.find_all('p'):
                if p.get('class') is None:
                    content += p.get_text() + " "
                
        #content type
        for div in soup.find_all('div', class_ = ['article_header_content']):
            for p in div.find_all('p', class_ = ['tag_title']):
                content_type = p.get_text()[28:]
            
                     
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
    
    urls_list = get_articles_urls(5) #récupération des urls des articles
    df = df_articles_content(urls_list) #récupéation du contenu des articles, stockage dans un dataframe
    
    path = os.getcwd()
    now = datetime.datetime.now().isoformat()
    filename = now[:10] + "_all_articles_lexpress" 
    save_as_json(df, path, filename) #sauvegarde en json du contenu des articles
    
    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" %(tps_e-tps_s))
