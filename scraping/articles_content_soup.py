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

def get_articles_urls():
    
    """ 
        Retourne une liste d'urls d'articles correspondant à la recherche 
        "coupe du monde 2022 qatar" sur le site "Le Monde"   
    """
    
    urls_list = []

    for i in range(1, 5): #range(1, 40) --> 400 articles
        url_search = 'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    
        for h3 in soup.find_all('h3'):
            for a in h3.find_all('a'):
                url = 'http://www.lemonde.fr' + a.get("href")
                urls_list.append(url)
                
    return(urls_list)
    
    
#☻Exécution
urls_list = get_articles_urls()
    

# =============================================================================
#                       Récupération du contenu des articles
# =============================================================================

def get_1_article_content(url):
    
    """ 
        Prend en entrée l'url d'un article
        Retourne un dictionnaire contenant : 
            source, url, date, thème, titre, sous-titre, contenu    
    """
    
    url_ = url
    soup = create_soup(url)
    source = "Le Monde"
    
    #date
    i = 0
    while i<100:
        if url[i].isdigit() == True:
            break
        i += 1
    date = url[i:i+10]
    
    #theme
    for li in soup.find_all('li'):
        if li.get("class") == ['breadcrumb__parent']:
            for a in li.find_all('a'):
                theme = a.get_text()
        
    #title
    title = soup.find('title').string
    
    #subtitle
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
            
    #dictionary        
    article_content = {"source": source,
                       "url": url_,
                       "date": date,
                       "theme": theme,
                       "title": title,
                       "subtitle": subtitle,
                       "content": content}

          
    return(article_content)
        

def list_articles_content(urls_list):
    
    """ 
        Prend en paramètre une liste d'urls d'articles
        Retourne une liste contenant un dictionnaire par article,
        chaque dictionnaire contenant : 
            source, url, date, thème, titre, sous-titre, contenu    
    """
    
    all_articles = []
    
    for url in urls_list:
        all_articles.append(get_1_article_content(url))
        
    return(all_articles)
        

#Exécution
all_articles = list_articles_content(urls_list)

#A FAIRE: fonction pour convertir la liste de dictionnaires en fichier json(?)
    
