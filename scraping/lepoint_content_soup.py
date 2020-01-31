# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:47:09 2019

==================================LE POINT=====================================

"""


from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import json
import time
import datetime
from datetime import datetime as dt2
%run functions.py



# =============================================================================
#             Récupération des URLs d'une recherche sur LePoint
# =============================================================================


def get_articles_urls(nb):
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant à la recherche 
        "qatar 2022" sur le site "Le Point" 
        tri par pertinence

    """

    urls_list = []

    for i in range(1, nb + 1):
        url_search = 'https://www.lepoint.fr/recherche/index.php?query=qatar+2022&sort=pertinence&page=' + \
            str(i)
        soup = create_soup(url_search)
        for article in soup.find_all('article'):
            for div in article.find_all('div'):
                if (div.get('class') is not None):
                    if 'pls' in div.get('class'):
                        for a in div.find_all('a'):
                            url = 'https://www.lepoint.fr' + a.get('href')
                            if url[:23] != 'https://www.lepoint.frh' and len(url) > 80:
                                urls_list.append(url)

    urls_list = list(set(urls_list))
    return(urls_list)



# =============================================================================
#                       Récupération du contenu des articles
# =============================================================================


def get_1_article_content(url):
    """ 
        Prend en entrée l'url d'un article
        Retourne : source, url, date, thème, titre, sous-titre, contenu, abo, type de contenu   

    """

    soup = create_soup(url)
    source = 'Le Point'
    date, theme, title, subtitle, content, abo, content_type = '', '', '', '', '', '', 'article'

    try:
        # date
        for div in soup.find_all('div', class_=['reset-text art-date-infos mts']):
            date = div.find('time').get_text()[:10]
            date = dt2.strptime(date, '%d/%m/%Y').strftime'%Y/%m/%d')

        # theme
        for nav in soup.find_all('nav', class_=['breadcrumb list-view mbm normal']):
            for a in nav.find_all('a'):
                theme += a.get_text()[1:] + ','

        # title
        if soup.find('h1', class_='art-titre list-view') is not None:
            title = soup.find(
                'h1', class_='art-titre list-view').get_text()[1:]

        # subtitle
        if soup.find('h2', class_='art-chapeau') is not None:
            subtitle = soup.find('h2', class_='art-chapeau').get_text()[1:]

        # content
        for div in soup.find_all('div', class_='art-text'):
            for p in div.find_all('p'):
                p = p.get_text()
                if p.find('©') != -1 and p.find('(') != -1 and p.find('/') != -1 and p.find(':') != -1:
                    content += ''
                else:
                    content += p + ' '

        # abo
        if soup.find('aside', id='article-reserve-aux-abonnes') is None:
            abo = 'non'
        else:
            abo = 'oui'

    except:
        print('Exception : ' + url + '\n')

    return(str(source), str(url), str(date), str(theme), str(title), str(subtitle), str(content), str(abo), str(content_type))


def df_articles_content(urls_list):
    """ 
        Prend en entrée une liste d'urls d'articles
        avec en colonnes : 
            source, url, date, thème, titre, sous-titre, contenu, abo, type de contenu  

    """

    df = pd.DataFrame(columns=['source', 'url', 'date', 'theme',
                               'title', 'subtitle', 'content', 'abo', 'content_type'])

    for url in urls_list:
        s, u, d, t, ti, su, c, a, ct = get_1_article_content(url)
        i = df.shape[0]
        df.loc[i+1] = [s, u, d, t, ti, su, c, a, ct]

    return(df)


        
# =============================================================================
#                             Exécution des fonctions
# =============================================================================


if __name__ == '__main__':
    tps_s = time.perf_counter()

    urls_list = get_articles_urls(53)  # récupération des urls des articles
    # récupéation du contenu des articles, stockage dans un dataframe
    df = df_articles_content(urls_list)

    path = os.getcwd()
    now = datetime.datetime.now().isoformat()
    filename = now[:10] + '_all_articles_lepoint'
    # sauvegarde en json du contenu des articles
    save_as_json(df, path, filename)

    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" % (tps_e - tps_s))