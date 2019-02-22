# cdm2022qatar

SCRAPING 
Entrée : site web avec recherche
Sortie : fichier .json structuré comme ceci:
          - dictionnaire avec 9 éléments : source, url, date, theme, title, subtitle, content, abo, content_type
          - chaque élément est de taille n avec n = nombre d'articles pour un site web donné

Liste des éléments : 
source : site web
url : url de l'article
date : date de publication de l'article - format YYYY/MM/DD
theme : catégorie(s) de l'article sur le site web - format : différentes catégories déparées par des ","
title : titre de l'article
subtitle : "chapeau" de l'article : une ou plusieurs phrase d'introduction ou de résumé
content : corps de texte de l'article
abo : article réservé aux abonnées - format : "oui" ou "non"
content_type : sur les sites ayant des types de contenu spéciaux, ex Courrier International : article, une, breve, dessin - par défaut : "article"

