# cdm2022qatar

## SCRAPING

algos d'extraction : dossier scraping > fichiers nomsite_content_soup.py

résultats à utiliser pour le nettoyage : dossier scraping > json > fichiers date_nomsite_allarticles.json

### Avancement
- 20 minutes ==> json OK

- Courrier International ==> json OK

- Le Monde ==> json OK

- L'Express ==> json OK

- L'Equipe ==> algo OK mais ne fonctionne pas sur certains articles, correction en cours

- Le Point ==> algo OK mais les 53 pages / 526 articles annoncés sur le site ne sortent pas tous, correction en cours

- Eurosport ==> urls OK, algo extraction en cours
   
   
---

     
**Fichiers .json structurés comme ceci :**

- **dictionnaire avec 9 éléments : source, url, date, theme, title, subtitle, content, abo, content_type**

- **chaque élément est de taille n avec n = nombre d'articles pour un site web donné**
   
   
---

          
Liste des éléments : 

- source : site web

- url : url de l'article

- date : date de publication de l'article - format YYYY/MM/DD

- theme : catégorie(s) de l'article sur le site web - format : différentes catégories séparées par des ","

- title : titre de l'article

- subtitle : "chapeau" de l'article : une ou plusieurs phrases d'introduction ou de résumé

- content : corps de texte de l'article

- abo : article réservé aux abonnés - format : "oui" ou "non"

- content_type : sur les sites ayant des types de contenu spéciaux, ex Courrier International : article, une, breve, dessin - par défaut : "article"

