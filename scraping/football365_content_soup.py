# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:59:35 2019

=================================FOOTBALL365===================================

"""


# =============================================================================
#                                 Librairies
# =============================================================================


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


# =============================================================================
#                     Récupération du code source d'une page
# =============================================================================


def create_soup(url):
    """ 
        Prend en entrée l'url d'une page web
        Retourne son code source  

    """

    req = requests.get(url)
    data = req.text
    soup = BeautifulSoup(data, 'lxml')
    return(soup)


# =============================================================================
#             Récupération des URLs d'une recherche sur un site web
# =============================================================================


def get_articles_urls(nb):
    """ 
        Prend en entrée le nombre de pages de recherche
        Retourne une liste d'urls d'articles correspondant à la recherche 
        "coupe du monde 2022 qatar" sur le site "Football 365"   

    """

    urls_list = []

    for i in range(1, nb + 1):
        url_search = 'http://www.football365.fr/page/' + \
            str(i) + '?s=coupe+du+monde+2022+qatar'
        soup = create_soup(url_search)
        div = soup.find('div', class_='row items-posts')
        for a in div.find_all('a', class_='new_tab_link hidden-xs'):
            url = a.get('data-href')
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
    source = 'football365'
    date, theme, title, subtitle, content, abo, content_type = '', '', '', '', '', 'non', 'article'

    try:
        # date
        date = soup.find('span', class_='date_article').get_text()[11:]
        k = date.find('à')
        date = date[:k-1]
        s = ['1er', 'Ã©', 'Ã»', 'janvier', 'février', 'avril',
             'juillet', 'septembre', 'octobre', 'novembre', 'décembre']
        t = ['1', 'é', 'û', 'janv.', 'févr.', 'avr.',
             'juil.', 'sept.', 'oct.', 'nov.', 'déc.']
        for i in range(11):
            date = date.replace(s[i], t[i])
        date = dt2.strptime(date, '%d %b %Y').strftime('%Y/%m/%d')
        while date[0] == ' ':
            date = date[1:]

        # theme
        ol = soup.find('ol', class_='breadcrumb-info')
        for span in ol.find_all('span'):
            theme += span.get_text() + ', '

        # title
        title = soup.find('h1', class_='title').get_text()[1:]

        # subtitle
        if soup.find('p', itemprop='description') is not None:
            subtitle = soup.find('p', itemprop='description').get_text()

        # content
        div = soup.find('div', itemprop='articleBody')
        for p in div.find_all('p'):
            if p.find_parent('blockquote', class_="twitter-tweet") is None:
                content += p.get_text()
        k = content.find('A voir aussi :')
        if k != -1:
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
        if c != '':
            df.loc[i+1] = [s, u, d, t, ti, su, c, a, ct]

    return(df)


# =============================================================================
#                              Sauvegarde en json
# =============================================================================


def save_as_json(df, path, filename):
    """
        Prend en entrée un dataframe
        Crée un fichier json avec le contenu du dataframe

    """

    data = df.to_dict()

    with open('{}/data/{}.json'.format(path, filename), 'w') as outfile:
        outfile.write(json.dumps(data, ensure_ascii=True, indent=4))


# =============================================================================
#                             Exécution des fonctions
# =============================================================================

if __name__ == '__main__':
    tps_s = time.perf_counter()

    urls_list = get_articles_urls(30)  # récupération des urls des articles 30
    # récupéation du contenu des articles, stockage dans un dataframe
    df = df_articles_content(urls_list)

    now = datetime.datetime.now().isoformat()
    filename = f'{now[:10]}_all_articles_football365'
    # sauvegarde en json du contenu des articles
    save_as_json(df, '', filename)

    tps_e = time.perf_counter()
    print("Temps d'execution (secondes) = %d\n" % (tps_e-tps_s))