# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 12:09:27 2019

https://code.tutsplus.com/fr/tutorials/scraping-webpages-in-python-with-beautiful-soup-the-basics--cms-28211

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
        Prend en entrée le nombre de pages de recherches
        Retourne une liste d'urls d'articles correspondant à la recherche 
        "coupe du monde 2022 qatar" sur le site "Le Monde"   
        
    """
    
    urls_list = []

    for i in range(1, nb+1): #40 pages
        url_search = 'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    
        for h3 in soup.find_all('h3'):
            for a in h3.find_all('a'):
                url = 'http://www.lemonde.fr' + a.get("href")
                urls_list.append(url)
                
    return(urls_list)
    

# =============================================================================
#                       Récupération du contenu des articles
# =============================================================================

def get_1_article_content(url):
    
    """ 
        Prend en entrée l'url d'un article
        Retourne : source, url, date, thème, titre, sous-titre, contenu    
    """
    
    url_ = url
    soup = create_soup(url)
    source = "Le Monde"
    
    try:
        #date
        date = ""
        i = 0
        while i<100:
            if url[i].isdigit() == True:
                break
            i += 1
        date = url[i:i+10]
        
        #theme
        theme = ""
        for li in soup.find_all('li'):
            if li.get("class") == ['breadcrumb__parent']:
                for a in li.find_all('a'):
                    theme = a.get_text()
            
        #title
        title = ""
        title = soup.find('title').string
        
        #subtitle - A MODIFIER y a des choses en trop
        subtitle = ""
        for main in soup.find_all('main'):
            for p in main.find_all('p'):
                if p.get("class") != ['article__status']:
                    if p.get("class") == ['article__desc']:
                        subtitle = p
                        
        #content - A MODIFIER y a des choses en trop
        content = ""
        for body in soup.find_all('body'):
            if body.get("id") == 'js-body':
                for article in body.find_all('article'):
                    if article.get("class") == ['article article--single article--iso']:
                        article.string = ""
                content += article.get_text() + " "
                
    except:
        print("Exception : " + url_+ "\n")
            
    return(str(source), str(url_), str(date), str(theme), str(title), str(subtitle), str(content))
               

def list_articles_content(urls_list):
    
    """ 
        Prend en entrée une liste d'urls d'articles
        avec en colonnes : 
            source, url, date, thème, titre, sous-titre, contenu    
    """
    
    df = pd.DataFrame(columns=['source', 'url', 'date','theme', 'title','subtitle','content'])
    
    for url in urls_list:
        s, u, d, t, ti, su, c = get_1_article_content(url)
        i = df.shape[0]
        df.loc[i+1] = [s, u, d, t, ti, su, c]

    return(df)
    
    
# =============================================================================
#                              Sauvegarde en json
# =============================================================================

def save_as_json(data, path, filename):

    """
        Prend en entrée un dictionnaire
        Crée un fichier json avec le contenu du dictionnaire
        
    """
    
    with open('{}\\data\\{}.json'.format(path, filename), 'w') as outfile:
        outfile.write(json.dumps(data, ensure_ascii = True, indent = 4))


# =============================================================================
#                             Exécution des fonctions
# =============================================================================

if __name__ == '__main__':
    tps_s = time.perf_counter()
    
    urls_list = get_articles_urls(20) #récupération des urls des articles (20 pages de recherche)
    df = list_articles_content(urls_list) #récupéation du contenu des articles, stockage dans un dataframe
    all_articles_dict = df.to_dict() #création d'un dictionnaire à partir du dataframe
    
    path = os.getcwd()
    now = datetime.datetime.now().isoformat()
    filename = "all_articles_" + now[:10]
    save_as_json(all_articles_dict, path, filename) #sauvegarde en json du contenu des articles
    
    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" %(tps_e-tps_s))
