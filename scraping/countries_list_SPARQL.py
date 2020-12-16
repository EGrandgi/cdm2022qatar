# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:42:28 2019

"""


from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import os
import datetime


# =============================================================================
#                Récupération de la liste des pays avec SPARQL
# =============================================================================


def SPARQL_exec():
    """
        Extrait la liste des pays et continents sur Wikipedia
        Requête générée automatiquement grâce au Wikidata Query Service
        (https://query.wikidata.org)

    """

    endpoint_url = 'https://query.wikidata.org/sparql'

    query = """
    SELECT DISTINCT ?countryLabel ?continentLabel WHERE {
      ?country wdt:P31 wd:Q3624078.
      OPTIONAL { ?country wdt:P30 ?continent. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". }
      FILTER(NOT EXISTS { ?country wdt:P31 wd:Q3024240. })
      FILTER(NOT EXISTS { ?country wdt:P31 wd:Q28171280. })
    }
    ORDER BY ?countryLabel"""

    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def results_into_df(results):
    """
        Entrée : résultats de la requête SPARQL  
        Sortie : dataframe

    """

    df = pd.DataFrame(columns=['country', 'continent'])

    for result in results['results']['bindings']:
        try:
            cy = result['countryLabel']['value']
            ct = result['continentLabel']['value']
            i = df.shape[0]
            df.loc[i+1] = [cy, ct]
        except:
            ''

    except_ = [14, 39, 68, 84, 122, 130, 134,
               135, 137, 138, 146, 149, 189, 202, 207]
    for e in except_:
        df = df.drop(e)

    df.loc[209]['country'] = 'Palestine'
    df.loc[209]['continent'] = 'Asie'

    df.reset_index(drop=True, inplace=True)

    df.loc[11]['continent'] = 'Océanie'

    return df


# =============================================================================
#                        Exécution et sauvegarde en csv
# =============================================================================

if __name__ == '__main__':

    results = SPARQL_exec()
    df = results_into_df(results)
    now = datetime.datetime.now().isoformat()
    filename = f'{now[:10]}_countries_list.csv'
    df.to_csv(os.path.join(os.path.abspath('..'), 'data', filename),
              encoding='utf-8', index=True, sep=';')