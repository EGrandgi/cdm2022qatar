# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:47:09 2019

================================RMC SPORT BFMTV================================

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
#             Récupération des URLs d'une recherche sur RMC Sport
# =============================================================================


def get_articles_urls(nb):
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant à la recherche google
        coupe du monde 2022 qatar site:https://rmcsport.bfmtv.com

    """

    urls_list = []

    for i in range(0, nb):
        url_search = 'https://www.google.com/search?q=coupe+du+monde+2022+qatar+%22coupe+du+monde+2022%22+site:https://rmcsport.bfmtv.com&ei=gIdwXPf4I5OFjLsPgMSR4AI&start=' + \
            str(i) + '0'
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



# =============================================================================
#                       Récupération du contenu des articles
# =============================================================================


def get_1_article_content(url):
    """ 
        Prend en entrée l'url d'un article
        Retourne : source, url, date, thème, titre, sous-titre, contenu, abo, type de contenu   

    """

    soup = create_soup(url)
    source = 'RMCSport'
    date, theme, title, subtitle, content, abo, content_type = '', '', '', '', '', 'non', 'article'

    try:
        # date
        date = soup.find(
            'time', class_='metadata-date-published time').get_text()
        i = date.find('/')
        date = date[i-2:i+8]
        date = dt2.strptime(date, '%d/%m/%Y').strftime('%Y/%m/%d')

        # theme
        ul = soup.find('ul', class_='breadcrumb no-padding no-margin')
        for li in ul.find_all('li'):
            if li.a.get_text().find('RMC') == -1:
                theme += li.a.get_text()[8:] + ','

        # title
        title = soup.find(
            'h1', class_='title-ultra titre-article text-center').get_text()
        if title[:1] == '\n':
            title = title[2:]
        while title[0] == ' ':
            title = title[1:]

        # subtitle
        if soup.find('h2') is not None:
            subtitle = soup.find('h2').get_text()

        # content
        div = soup.find('div', itemprop='articleBody')
        for p in div.find_all('p'):
            content += p.get_text() + ' '
        if content == '':
            content += div.get_text() + ' '
            k = content.find('A lire aussi')
            content = content[:k]

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
        if d != '' and c != '':
            df.loc[i+1] = [s, u, d, t, ti, su, c, a, ct]

    return(df)



# =============================================================================
#                             Exécution des fonctions
# =============================================================================


if __name__ == '__main__':
    tps_s = time.perf_counter()

    urls_list = get_articles_urls(25)  # récupération des urls des articles
    # récupéation du contenu des articles, stockage dans un dataframe
    df = df_articles_content(urls_list)

    path = os.getcwd()
    now = datetime.datetime.now().isoformat()
    filename = now[:10] + '_all_articles_rmcsport'
    # sauvegarde en json du contenu des articles
    save_as_json(df, path, filename)

    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" % (tps_e - tps_s))