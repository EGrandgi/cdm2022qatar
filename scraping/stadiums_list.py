# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:42:28 2019

"""

# =============================================================================
#                                 Packages
# =============================================================================

import json
import os
import datetime


# =============================================================================
#                Création du dictionnaire de données sur les stades
# =============================================================================

stadiums_dict = {'city':{1:'Lusail',
                         2:'Doha',
                         3:'Doha',
                         4:'Doha',
                         5:'Al_Khor',
                         6:'Ash Shamal',
                         7:'Al Wakrah',
                         8:'Umm Salal',
                         9:'Doha',
                         10:'Doha',
                         11:'Al Rayyan',
                         12:'Doha'},
                'lib_stadium':{1:'Lusail Iconic Stadium',
                               2:'Khalifa International Stadium',
                               3:'Sports City Stadium',
                               4:'Education City Stadium', 
                               5:'Al-Khawr Stadium',
                               6:'Ash Shamal Stadium',
                               7:'Al-Wakrah Stadium',
                               8:'Umm Salal Stadium',
                               9:'Doha Port Stadium',
                               10:'Stade Thani bin Jassim',
                               11:'Stade Ahmed bin Ali',
                               12:'Qatar University Stadium'},       
                'capacity':{1:'86250',
                            2:'40000',
                            3:'47560',
                            4:'45350',
                            5:'45330',
                            6:'45120',
                            7:'45120',
                            8:'45120',
                            9:'44950',
                            10:'44740',
                            11:'44740',
                            12:'43520'},
                 'status':{1:'a_construire',
                          2:'renove',
                          3:'a_construire',
                          4:'a_construire',
                          5:'a_construire',
                          6:'a_construire',
                          7:'a_construire',
                          8:'a_construire',
                          9:'a_construire',
                          10:'a_agrandir',
                          11:'a_agrandir',
                          12:'a_construire'}}


# =============================================================================
#                               Convertir en json
# =============================================================================

def save_as_json(dict_, path, filename):

    """
        Entrée : dictionnaire
        Sortie : fichier json avec le contenu du dictionnaire
         
    """
        
    with open('{}\\data\\{}.json'.format(path, filename), 'w') as outfile:
        outfile.write(json.dumps(dict_, ensure_ascii = True, indent = 4))
        
      
# =============================================================================
#                                Exécution
# =============================================================================
        
if __name__ == '__main__':

    path = os.getcwd()
    now = datetime.datetime.now().isoformat()
    filename = now[:10] + "_stadiums_info"
    save_as_json(stadiums_dict, path, filename)

