# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 12:09:27 2019

https://code.tutsplus.com/fr/tutorials/scraping-webpages-in-python-with-beautiful-soup-the-basics--cms-28211

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
        url_search = 'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + str(i) +'&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=pertinence'
        soup = create_soup(url_search)
    
        for h3 in soup.find_all('h3'):
            for a in h3.find_all('a'):
                url = 'http://www.lemonde.fr' + a.get("href")
                urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


# =============================================================================
#                   Get urls for a specific search - L'EQUIPE
# =============================================================================

def get_articles_urls():
    urls_list = []

    for i in range(1, 5):
        url_search = 'https://www.lequipe.fr/recherche/search.php?r=coupe+du+monde+2022+qatar&jd=01&md=01&ad=2019&jf=01&mf=01&af=2019&t=ALL&adv=0&o=P&s=ALL&s1=efr&p=' + str(i)
        soup = create_soup(url_search)
    
        for h2 in soup.find_all('h2'):
            for a in h2.find_all('a'):
                url = 'https://www.lequipe.fr' + a.get("href")
                urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


# =============================================================================
#                   Get urls for a specific search - L'EXPRESS
# =============================================================================

def get_articles_urls():
    urls_list = []

    for i in range(1, 5):
        url_search = 'https://www.lexpress.fr/recherche?q=coupe+du+monde+2022+qatar&p=' + str(i)
        soup = create_soup(url_search)
        for div in soup.find_all('div'):
            if (div.get("class")!=None):
                if "img_container" in div.get("class"):
                    for a in div.find_all('a'):
                        url = a.get("href")
                        urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


# =============================================================================
#                   Get urls for a specific search - COURRIER INTERNATIONAL
# =============================================================================
#qatar 2022

def get_articles_urls():
    urls_list = []

    for i in range(0, 5):
        url_search = 'https://www.courrierinternational.com/search/result/qatar%202022?sort_bef_combine=changed%20DESC&sort_order=DESC&sort_by=changed&page=' + str(i)
        soup = create_soup(url_search)
        for article in soup.find_all('article'):
                    for a in article.find_all('a'):
                        url = 'https://www.courrierinternational.com' + a.get("href")
                        urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


# =============================================================================
#                   Get urls for a specific search - LE POINT
# =============================================================================
#qatar 2022

def get_articles_urls():
    urls_list = []

    for i in range(1, 3):
        url_search = 'https://www.lepoint.fr/recherche/index.php?query=qatar+2022&sort=pertinence&page=' + str(i)
        soup = create_soup(url_search)
        for article in soup.find_all('article'):
            for div in article.find_all('div'):
                if (div.get("class")!=None):
                    if 'pls' in div.get("class"):
                        for a in div.find_all('a'):
                            url = 'https://www.lepoint.fr' + a.get("href")
                            urls_list.append(url)
                
    return(urls_list)
    
urls_list = get_articles_urls()


# =============================================================================
#                   Get urls for a specific search - 20 MINUTES
# =============================================================================
#coupe du monde 2022 qatar "coupe du monde 2022" site:https://www.20minutes.fr/

def get_articles_urls():
    urls_list = []

    for i in range(0, 25):
        url_search = 'https://www.google.com/search?q=coupe+du+monde+2022+qatar+%22coupe+du+monde+2022%22+site:https://www.20minutes.fr/&lr=&hl=fr&as_qdr=all&ei=_U9tXNjSJJXAgweGj7OwBg&start=' + str(i) + '0'
        soup = create_soup(url_search)
    
        for a in soup.find_all('a'):
            if a.get('href')[:21] == '/url?q=https://www.20':
                urls_list.append(a.get('href')[7:])
                
    return(urls_list)
    
urls_list = get_articles_urls()


# =============================================================================
#                   Get urls for a specific search - EUROSPORT
# =============================================================================
#coupe du monde 2022 qatar "coupe du monde 2022" site:https://www.eurosport.fr/

def get_articles_urls():
    urls_list = []

    for i in range(0, 15):
        url_search = 'https://www.google.com/search?q=coupe+du+monde+2022+qatar+%22coupe+du+monde+2022%22+site:https://www.eurosport.fr/&lr=&hl=fr&as_qdr=all&ei=WFFtXPOHE8GxgweRoamYCg&start=' + str(i) + '0'
        soup = create_soup(url_search)
    
        for a in soup.find_all('a'):
            if a.get('href')[:21] == '/url?q=https://www.eu':
                urls_list.append(a.get('href')[7:])
                
    return(urls_list)
    
urls_list = get_articles_urls()


# =============================================================================
#                   Get urls for a specific search - RMCSPORT
# =============================================================================
#coupe du monde 2022 qatar site:https://rmcsport.bfmtv.com

def get_articles_urls():
    urls_list = []

    for i in range(0, 5):
        url_search = 'https://www.google.com/search?q=coupe+du+monde+2022+qatar+%22coupe+du+monde+2022%22+site:https://rmcsport.bfmtv.com&ei=gIdwXPf4I5OFjLsPgMSR4AI&start=' + str(i) + '0'
        soup = create_soup(url_search)
    
        for a in soup.find_all('a'):
            if a.get('href')[:21] == '/url?q=https://rmcspo':
                url = a.get('href')[7:]
                i = url.find('html')
                k = url.find('mediaplayer')
                if i != -1 and k == -1:
                    url = url[:i+4]
                    urls_list.append(url)
    
    urls_list = list(set(urls_list))  
                        
    return(urls_list)

urls_list = get_articles_urls()


# =============================================================================
#                  Get urls for a specific search - FOOTBALL365
# =============================================================================
#"coupe du monde 2022 qatar"

def get_articles_urls():
    urls_list = []

    for i in range(1, 5):
        url_search = 'http://www.football365.fr/page/' + str(i) + '?s=coupe+du+monde+2022+qatar'
        soup = create_soup(url_search)
        div = soup.find('div', class_ = 'row items-posts')
        for a in div.find_all('a', class_ = 'new_tab_link hidden-xs'):
            url = a.get('data-href')
            urls_list.append(url)
                            
    return(urls_list)

urls_list = get_articles_urls()


# =============================================================================
#                Get urls for a specific search - FRANCEFOOTBALL
# =============================================================================
#coupe du monde 2022 qatar "coupe du monde 2022 qatar "coupe du monde 2022" site:https://www.francefootball.fr"

def get_articles_urls():
    urls_list = []

    for i in range(0, 5):
        url_search = 'https://www.google.fr/search?q=coupe+du+monde+2022+qatar+%22coupe+du+monde+2022%22+site:https://www.francefootball.fr&ei=n4xwXJiZMK3PrgTw1oHoCg&start=' + str(i) + '0'
        soup = create_soup(url_search)
    
        for a in soup.find_all('a'):
            if a.get('href')[:21] == '/url?q=https://www.fr':
                url = a.get('href')[7:]
                k = url.find('&')
                url = url[:k]
                urls_list.append(url)
                            
    return(urls_list)

urls_list = get_articles_urls()
