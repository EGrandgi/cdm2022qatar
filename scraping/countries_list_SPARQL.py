# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:42:28 2019

"""

# =============================================================================
#                                 Packages
# =============================================================================

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import json
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
    
    endpoint_url = "https://query.wikidata.org/sparql"
    
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
    
    for result in results["results"]["bindings"]:
        try:
            cy = result["countryLabel"]["value"]
            ct = result["continentLabel"]["value"]
            i = df.shape[0]
            df.loc[i+1] = [cy, ct]
        except:
            ""
    
    except_ = [14, 39, 68, 84, 122, 130, 134, 135, 137, 138, 146, 149, 189, 202, 207, 209]
    for e in except_:
        df = df.drop(e)
    
    df.reset_index(drop=True, inplace=True)
    
    df.loc[11]['continent']= 'Océanie'
    
    return df


def save_as_json(df, path, filename):

    """
        Entrée : dataframe
        Sortie : fichier json avec le contenu du dataframe
         
    """
    
    data = df.to_dict()
    
    with open('{}\\data\\{}.json'.format(path, filename), 'w') as outfile:
        outfile.write(json.dumps(data, ensure_ascii = True, indent = 4))
        
        
        
if __name__ == '__main__':

    results = SPARQL_exec()
    df = results_into_df(results)
    path = os.getcwd()
    now = datetime.datetime.now().isoformat()
    filename = now[:10] + "_countries_list"
    save_as_json(df, path, filename)

