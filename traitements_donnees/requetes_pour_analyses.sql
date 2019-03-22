SELECT COUNT(*) FROM ARTICLES;
--- 2944 articles

SELECT COUNT(*) FROM TIME_;
--- 1046 dates distinctes

SELECT COUNT(*) FROM DATER_DE;
--- 2944 lignes : 1 article associé à 1 date

SELECT COUNT(*) FROM COUNTRIES;
--- 197 pays

SELECT COUNT(*) FROM PROVENIR_DE;
--- 2944 lignes : 1 article associé à 1 pays

SELECT COUNT(*) FROM PERSONS;
--- 305 personnes

SELECT COUNT(*) FROM CONCERNER_PE;
--- 5463 associations article-personne

SELECT COUNT(*) FROM PLACES;
--- 12 stades

SELECT COUNT(*) FROM CONCERNER_PL;
--- 58 associations article-stade


SELECT source_, COUNT(*) FROM ARTICLES GROUP BY source_;
--- nombre d'articles par source
--- LExpress				1009
--- Le Monde				412
--- lequipe					377
--- football365				262
--- 20 minutes				199
--- RMCSport				188
--- Le Point				158
--- France Football			144
--- Eurosport				141
--- Courrier International	54

SELECT id_pers, COUNT(*) FROM CONCERNER_PE GROUP BY id_pers;
--- identifiants des personnes concernées
--- 148     				717
--- 204         			488
--- 139     				202
--- 55     	    			195
--- 118     				188
--- 199      				166

SELECT id_pers, pers FROM PERSONS WHERE id_pers = '148';    --- joseph_blatter
SELECT id_pers, pers FROM PERSONS WHERE id_pers = '204';    --- michel_platini
SELECT id_pers, pers FROM PERSONS WHERE id_pers = '139';    --- jerome_valcke
SELECT id_pers, pers FROM PERSONS WHERE id_pers = '55';     --- bin_hammam
SELECT id_pers, pers FROM PERSONS WHERE id_pers = '118';    --- gianni_infantino
SELECT id_pers, pers FROM PERSONS WHERE id_pers = '199';    --- michael_garcia

SELECT SUBSTR(date_, 7) AS Y, COUNT(*) FROM DATER_DE GROUP BY SUBSTR(date_, 7);
--- nb d'articles par année
--- 2010        87
--- 2011        145
--- 2012        53
--- 2013        284
--- 2014        692
--- 2015        663
--- 2016        237
--- 2017        246
--- 2018        303
--- 2019        234