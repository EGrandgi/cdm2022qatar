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

    for i in range(1, 40):
        url_search = 'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    
        for h3 in soup.find_all('h3'):
            for a in h3.find_all('a'):
                url = 'http://www.lemonde.fr' + a.get("href")
                urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


url = urls_list[4]
soup = create_soup(url)

# =============================================================================
#                   Get urls for a specific search - L'EQUIPE
# =============================================================================

def get_articles_urls():
    urls_list = []

    for i in range(1, 5):
        url_search = 'https://www.lequipe.fr/recherche/search.php?r=coupe+du+monde+2022+qatar&jd=01&md=01&ad=2019&jf=01&mf=01&af=2019&t=ALL&adv=0&o=D&s=ALL&s1=efr&p=' + str(i)
        #'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    
        for h2 in soup.find_all('h2'):
            for a in h2.find_all('a'):
                url = 'https://www.lequipe.fr' + a.get("href")
                urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


url = urls_list[4]
soup = create_soup(url)

# =============================================================================
#                   Get urls for a specific search - L'EXPRESS
# =============================================================================

def get_articles_urls():
    urls_list = []

    for i in range(1, 5):
        url_search = 'https://www.lexpress.fr/recherche?q=coupe+du+monde+2022+qatar&p=' + str(i)
        #'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    #<div class="group">
        for div in soup.find_all('div'):
            if (div.get("class")!=None):
                if "img_container" in div.get("class"):
                    for a in div.find_all('a'):
                        url = a.get("href")
                        urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


url = urls_list[4]
soup = create_soup(url)

# =============================================================================
#                   Get urls for a specific search - COURRIER INTERNATIONAL
# =============================================================================
#qatar 2022

def get_articles_urls():
    urls_list = []

    for i in range(0, 5):
        url_search = 'https://www.courrierinternational.com/search/result/qatar%202022?sort_bef_combine=changed%20DESC&sort_order=DESC&sort_by=changed&page=' + str(i)
        #'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    #<div class="group">
        for article in soup.find_all('article'):
                    for a in article.find_all('a'):
                        url = 'https://www.courrierinternational.com' + a.get("href")
                        urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


url = urls_list[4]
soup = create_soup(url)

# =============================================================================
#                   Get urls for a specific search - LE POINT
# =============================================================================
#qatar 2022

def get_articles_urls():
    urls_list = []

    for i in range(1, 3):
        url_search = 'https://www.lepoint.fr/recherche/index.php?query=qatar+2022&sort=pertinence&page=' + str(i)
        #'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=desc'
        soup = create_soup(url_search)
    #<div class="group">
        for article in soup.find_all('article'):
            for div in article.find_all('div'):
                if (div.get("class")!=None):
                    if 'pls' in div.get("class"):
                        for a in div.find_all('a'):
                            url = 'https://www.lepoint.fr' + a.get("href")
                            urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


url = urls_list[4]
soup = create_soup(url)

# =============================================================================
#                   Get urls for a specific search - 20 MINUTES
# =============================================================================


# (pas fini)

#def get_articles_urls():
#    urls_list = []
#
#    for i in range(1, 6):
#        url_search = 'https://www.20minutes.fr/search?q=coupe+du+monde+2022+qatar'
#        soup = create_soup(url_search)
#    
#        for div in soup.find_all('div'):
#            for class in div.find_all('div')
#            url = 'https://www.20minutes.fr' + class.get("gsc-url-top")
#            urls_list.append(url)
#                
#    return(urls_list)
#    
#urls_list = get_articles_urls()
#
#
#url = urls_list[4]
#soup = create_soup(url)
    