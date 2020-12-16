# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 17:44:38 2019

=================================L'EXPRESS=====================================

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
#             Récupération des URLs d'une recherche sur L'Express
# =============================================================================


def get_articles_urls(nb, nb_):
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant aux recherches 
        "coupe du monde 2022 qatar" et "Mondial-2022" sur le site "L'Express"   

    """

    urls_list = []

    for i in range(1, nb + 1):
        url_search = 'https://www.lexpress.fr/recherche?q=coupe+du+monde+2022+qatar&p=' + \
            str(i)
        soup = create_soup(url_search)
        for div in soup.find_all('div'):
            if (div.get('class') is not None):
                if 'img_container' in div.get('class'):
                    for a in div.find_all('a'):
                        url = a.get('href')
                        urls_list.append(url)

    for i in range(1, nb_ + 1):
        url_search = 'https://www.lexpress.fr/recherche?q=Mondial-2022&p=' + \
            str(i)
        soup = create_soup(url_search)
        for div in soup.find_all('div'):
            if (div.get('class') is not None):
                if 'img_container' in div.get('class'):
                    for a in div.find_all('a'):
                        url = a.get('href')
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
    source = 'LExpress'
    date, theme, title, subtitle, content, abo, content_type = '', '', '', '', '', 'non', 'article'

    try:
        # date
        for time_ in soup.find_all('time', itemprop='datePublished'):
            date = time_.get_text()[9:19]
            date = dt2.strptime(date, '%d/%m/%Y').strftime('%Y/%m/%d')

        # theme
        for nav in soup.find_all('nav', class_='breadcrumb'):
            for li in nav.find_all('li'):
                theme += li.get_text() + ','

        # title
        title = soup.find('h1', class_='title_alpha').get_text()[11:]

        # subtitle
        subtitle = soup.find('h2', class_='chapo title_gamma').get_text()[11:]

        # content
        for div in soup.find_all('div', class_='article_container'):
            for p in div.find_all('p'):
                if p.get('class') is None:
                    content += p.get_text() + ' '

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

    urls_list = get_articles_urls(20, 5)  # récupération des urls des articles
    # récupéation du contenu des articles, stockage dans un dataframe
    df = df_articles_content(urls_list)

    now = datetime.datetime.now().isoformat()
    filename = f'{now[:10]}_all_articles_lexpress'
    # sauvegarde en json du contenu des articles
    save_as_json(df, '', filename)

    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" % (tps_e - tps_s))