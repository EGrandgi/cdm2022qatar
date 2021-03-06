# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:59:35 2019

=============================COURRIER INTERNATIONAL============================

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
#        Récupération des URLs d'une recherche sur Courrier International
# =============================================================================


def get_articles_urls(nb):
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant à la recherche 
        "qatar 2022" sur le site "Courrier International"   

    """

    urls_list = []

    for i in range(1, nb + 1):
        url_search = 'https://www.courrierinternational.com/search/result/qatar%202022?sort_bef_combine=changed%20DESC&sort_order=DESC&sort_by=changed&page=' + \
            str(i)
        soup = create_soup(url_search)
        for article in soup.find_all('article'):
            for a in article.find_all('a'):
                url = 'https://www.courrierinternational.com' + a.get('href')
                urls_list.append(url)

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
    source = 'Courrier International'
    date, theme, title, subtitle, content, abo, content_type = '', '', '', '', '', '', ''

    try:
        # content type
        init = ['u', 'a', 'b', 'd', 'g']
        t = ['une', 'article', 'breve', 'dessin', 'galerie']
        for i in range(5):
            if url[38:39] == init[i]:
                content_type = t[i]

        # date
        for time_ in soup.find_all('time', itemprop='datePublished'):
            date = time_.get_text()[:10]
            date = dt2.strptime(date, '%d/%m/%Y').strftime('%Y/%m/%d')

        # theme
        if content_type != 'dessin':
            if content_type != 'galerie':
                for ul in soup.find('ul', class_='breadcrumbs'):
                    for span in ul.find_all('span', itemprop='name'):
                        theme += span.get_text() + ', '

        # title
        title = soup.find('h1', class_='article-title').get_text()

        # subtitle
        if soup.find('p', class_='article-lede') is not None:
            subtitle = soup.find('p', class_='article-lede').get_text()

        # content
        for div in soup.find_all('div', class_='article-text'):
            for p in div.find_all('p'):
                content += p.get_text() + ' '

        # abo
        if soup.find('div', class_='box-reserved-abo') is None:
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

    urls_list = get_articles_urls(7)  # récupération des urls des articles
    # récupéation du contenu des articles, stockage dans un dataframe
    df = df_articles_content(urls_list)

    now = datetime.datetime.now().isoformat()
    filename = f'{now[:10]}_all_articles_courrierint'
    # sauvegarde en json du contenu des articles
    save_as_json(df, '', filename)

    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" % (tps_e - tps_s))