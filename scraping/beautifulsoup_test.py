# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 12:09:27 2019

https://code.tutsplus.com/fr/tutorials/scraping-webpages-in-python-with-beautiful-soup-the-basics--cms-28211

@author: EGrandgi
"""

# =============================================================================
#                                   Packages
# =============================================================================

from bs4 import BeautifulSoup
import requests
import re


# =============================================================================
#                                Create soup
# =============================================================================

def create_soup(url):
    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, "lxml")
    return(soup)


# =============================================================================
#                   Get urls for a specific search - LE MONDE
# =============================================================================

def get_articles_urls():
    urls_list = []

    for i in range(1, 2):
        url_search = 'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    
        for h3 in soup.find_all('h3'):
            for a in h3.find_all('a'):
                url = 'http://www.lemonde.fr' + a.get("href")
                urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()

                
# =============================================================================
#                     Get the articles' content - LE MONDE
# =============================================================================

def get_articles_content():
    
    for url in urls_list:
        soup = create_soup(url)
        source = "Le Monde"
        
        #title
        title = soup.find('title').string
        
        #subtitle
        for main in soup.find_all('main'):
            for p in main.find_all('p'):
                if p.get("class") != ['article__status']:
                    if p.get("class") == ['article__desc']:
                        subtitle = p
                    
        return(source, url, title, subtitle)
        
        

data = get_articles_content()




article_content = { "source": source,
                    "url": url,
#                    "author": author,
#                    "date": date,
#                    "category": category,
                    "title": title,
                    "subtitle": subtitle}
#                    "content": content }
