# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:47:09 2019

===============================FRANCE FOOTBALL=================================

"""


from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import json
import time
import datetime
from datetime import datetime as dt2
import locale
locale.setlocale(locale.LC_TIME, '')
%run functions.py


# =============================================================================
#             Récupération des URLs d'une recherche sur France Football
# =============================================================================


def get_articles_urls(nb):
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant à la recherche google
        coupe du monde 2022 qatar "coupe du monde 2022 qatar "coupe du monde 2022" site:https://www.francefootball.fr"

    """

    urls_list = []

    for i in range(0, nb):
        url_search = 'https://www.google.fr/search?q=coupe+du+monde+2022+qatar+%22coupe+du+monde+2022%22+site:https://www.francefootball.fr&ei=n4xwXJiZMK3PrgTw1oHoCg&start=' + \
            str(i) + '0'
        soup = create_soup(url_search)

        for a in soup.find_all('a'):
            if a.get('href')[:21] == '/url?q=https://www.fr':
                url = a.get('href')[7:]
                k = url.find('&')
                url = url[:k]
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
    source = 'France Football'
    date, theme, title, subtitle, content, abo, content_type = '', '', '', '', '', 'non', 'article'

    try:
        # date
        date = soup.find(
            'div', class_='sidebar__date js-analytics-timestamp').get_text()
        k = date.find('&')
        date = date[3:k-1]
        s = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        t = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin',
             'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']
        for i in range(12):
            date = date.replace(s[i], t[i])
        date = dt2.strptime(date, '%d %b %Y').strftime('%Y/%m/%d')

        # theme
        theme = soup.find(
            'span', class_='strapline__item strapline__item--compet').get_text()

        # title
        title = soup.find(
            'h1', class_='heading strapline__item strapline__item--title').get_text()

        # subtitle
        if soup.find('p', class_='paragraph paragraph--chapo') is not None:
            subtitle = soup.find(
                'p', class_='paragraph paragraph--chapo').get_text()

        # content
        for div in soup.find_all('div', class_='paragraph'):
            content += div.get_text() + ' '

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
        if d != '':
            df.loc[i+1] = [s, u, d, t, ti, su, c, a, ct]

    return(df)


# =============================================================================
#                             Exécution des fonctions
# =============================================================================

if __name__ == '__main__':
    tps_s = time.perf_counter()

    urls_list = get_articles_urls(16)  # récupération des urls des articles
    # récupéation du contenu des articles, stockage dans un dataframe
    df = df_articles_content(urls_list)

    now = datetime.datetime.now().isoformat()
    filename = f'{now[:10]}_all_articles_francefootball'
    # sauvegarde en json du contenu des articles
    save_as_json(df, '', filename)

    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" % (tps_e - tps_s))