# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 11:04:21 2019

"""


from bs4 import BeautifulSoup
import requests



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