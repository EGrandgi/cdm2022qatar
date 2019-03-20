------------------------------------------------------------------------------------------------------------------------------
-- 												Création base de données CDMQATAR2022
------------------------------------------------------------------------------------------------------------------------------

DROP TABLE CONCERNER_PL;
DROP TABLE CONCERNER_PE;
DROP TABLE DATER_DE;
DROP TABLE PROVENIR_DE;
DROP TABLE COUNTRIES;
DROP TABLE PERSONS;
DROP TABLE PLACES;
DROP TABLE TIME_;
DROP TABLE ARTICLES;


------------------------------------------------------------------------------------------------------------------------------
-- 														Table COUNTRIES
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE COUNTRIES(
	id_country       			VARCHAR(5),
	country       				VARCHAR(40),
	continent				VARCHAR(16),

	CONSTRAINT PK_CONSTRAINT_COUNTRIES PRIMARY KEY (id_country)
);
	
------------------------------------------------------------------------------------------------------------------------------
-- 														Table PERSONS
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE PERSONS(
	id_pers					VARCHAR(5),
	pers					VARCHAR(30),

	CONSTRAINT PK_CONSTRAINT_PERSONS PRIMARY KEY (id_pers)
);
	
------------------------------------------------------------------------------------------------------------------------------
-- 														Table PLACES
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE PLACES(
	id_stadium				VARCHAR(5),
	stadium					VARCHAR(50),
	city					VARCHAR(20),
	capacity_				VARCHAR(10),
	status_					VARCHAR(20),

	CONSTRAINT PK_CONSTRAINT_PLACES PRIMARY KEY (id_stadium)
);
	
------------------------------------------------------------------------------------------------------------------------------
-- 														Table TIME_
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE TIME_(
	date_					VARCHAR(10),
	year_					VARCHAR(5),
	month_					VARCHAR(5),
	day_					VARCHAR(5),
	
	CONSTRAINT PK_CONSTRAINT_TIME_ PRIMARY KEY (date_)
);
	
------------------------------------------------------------------------------------------------------------------------------
-- 														Table ARTICLES
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE ARTICLES(
	id_article				VARCHAR(5),
	date_					VARCHAR(10),
	source_					VARCHAR(30),
	url_					VARCHAR(300),
	title					VARCHAR(200),
	subtitle				VARCHAR(1000),
    	content_cut     		        VARCHAR(4000), 
	abo					VARCHAR(3),
	content_type				VARCHAR(15),
	theme					VARCHAR(1000),
	
	CONSTRAINT PK_CONSTRAINT_ARTICLES PRIMARY KEY (id_article)
);

------------------------------------------------------------------------------------------------------------------------------
-- 														Table DATER_DE
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE DATER_DE(
	id_article				VARCHAR(5),
	date_					VARCHAR(10),
	
	CONSTRAINT PK_CONSTRAINT_DATER_DE PRIMARY KEY (id_article, date_)
);

------------------------------------------------------------------------------------------------------------------------------
-- 														Table PROVENIR_DE
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE PROVENIR_DE(
	id_article				VARCHAR(5),
	id_country				VARCHAR(5),
	
	CONSTRAINT PK_CONSTRAINT_PROVENIR_DE PRIMARY KEY (id_article, id_country)
);

------------------------------------------------------------------------------------------------------------------------------
-- 														Table CONCERNER_PE
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE CONCERNER_PE(
	id_article				VARCHAR(5),
	id_pers					VARCHAR(5),
	
	CONSTRAINT PK_CONSTRAINT_CONCERNER_PE PRIMARY KEY (id_article, id_pers)
);

------------------------------------------------------------------------------------------------------------------------------
-- 														Table CONCERNER_PL
------------------------------------------------------------------------------------------------------------------------------
CREATE TABLE CONCERNER_PL(
	id_article				VARCHAR(5),
	id_stadium				VARCHAR(5),
	
	CONSTRAINT PK_CONSTRAINT_CONCERNER_PL PRIMARY KEY (id_article, id_stadium)
);
	
------------------------------------------------------------------------------------------------------------------------------
-- 														Clés étrangères
------------------------------------------------------------------------------------------------------------------------------
	
ALTER TABLE DATER_DE ADD CONSTRAINT FK_DATER_DE_id_article FOREIGN KEY (id_article) REFERENCES ARTICLES(id_article);
ALTER TABLE DATER_DE ADD CONSTRAINT FK_DATER_DE_date_ FOREIGN KEY (date_) REFERENCES TIME_(date_);

ALTER TABLE PROVENIR_DE ADD CONSTRAINT FK_PROVENIR_DE_id_article FOREIGN KEY (id_article) REFERENCES ARTICLES(id_article);
ALTER TABLE PROVENIR_DE ADD CONSTRAINT FK_PROVENIR_DE_id_country FOREIGN KEY (id_country) REFERENCES COUNTRIES(id_country);

ALTER TABLE CONCERNER_PE ADD CONSTRAINT FK_CONCERNER_PE_id_article FOREIGN KEY (id_article) REFERENCES ARTICLES(id_article);
ALTER TABLE CONCERNER_PE ADD CONSTRAINT FK_CONCERNER_PE_id_pers FOREIGN KEY (id_pers) REFERENCES PERSONS(id_pers);

ALTER TABLE CONCERNER_PL ADD CONSTRAINT FK_CONCERNER_PL_id_article FOREIGN KEY (id_article) REFERENCES ARTICLES(id_article);
ALTER TABLE CONCERNER_PL ADD CONSTRAINT FK_CONCERNER_PL_id_stadium FOREIGN KEY (id_stadium) REFERENCES PLACES(id_stadium);
