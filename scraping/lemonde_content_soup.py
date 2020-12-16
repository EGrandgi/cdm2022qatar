# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 12:09:27 2019

==================================LE MONDE=====================================

"""


from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import datetime
import json
import time
%run functions.py


# =============================================================================
#             Récupération des URLs d'une recherche sur LeMonde
# =============================================================================


def get_articles_urls(nb):
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant à la recherche 
        "coupe du monde 2022 qatar" sur le site "Le Monde"  
        tri par pertinence

    """

    urls_list = []

    for i in range(1, nb + 1):  # 40 pages
        url_search = 'https://www.lemonde.fr/recherche/?keywords=coupe+du+monde+2022+qatar&page_num=' + \
            str(i) + '&operator=and&exclude_keywords=&qt=recherche_texte_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=29&end_month=01&end_year=2019&sort=pertinence'
        soup = create_soup(url_search)

        for h3 in soup.find_all('h3'):
            for a in h3.find_all('a'):
                url = 'http://www.lemonde.fr' + a.get('href')
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
    source = 'Le Monde'
    date, theme, title, subtitle, content, abo, content_type = '', '', '', '', '', '', 'article'

    try:
        # date
        i = 0
        while i < 100:
            if url[i].isdigit():
                break
            i += 1
        date = url[i:i+10]

        # theme
        for ul in soup.find_all('ul', class_='breadcrumb'):
            for a in ul.find_all('a'):
                theme += a.get_text() + ','

        # title
        title = soup.find('title').get_text()

        # subtitle
        for p in soup.find_all('p', class_='article__desc'):
            subtitle = p.get_text()

        #content & abo
        for section in soup.find_all('section', class_=['article__content', 'old__article-content-single']):
            for p in section.find_all('p'):
                if p.get('class') == 'article__status':
                    abo += 'oui'
                if p.span is None:
                    content += p.get_text() + ' '
        if abo == '':
            abo = 'non'

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

    urls_list = get_articles_urls(42)  # récupération des urls des articles
    # récupéation du contenu des articles, stockage dans un dataframe
    df = df_articles_content(urls_list)

    now = datetime.datetime.now().isoformat()
    filename = f'{now[:10]}_all_articles_lemonde'
    # sauvegarde en json du contenu des articles
    save_as_json(df, '', filename)

    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" % (tps_e - tps_s))