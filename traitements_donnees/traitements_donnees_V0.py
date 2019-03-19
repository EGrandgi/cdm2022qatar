# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 08:25:53 2019

"""

# =============================================================================
#                                 Packages
# =============================================================================

import pandas as pd
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
import re
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
import pyLDAvis
import pyLDAvis.gensim
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer


# =============================================================================
#                                  Données
# =============================================================================

path = 'C:\\Users\\Etudiant\\data\\'
df_articles = pd.DataFrame.from_csv(path + '2019-03-19_articles_clean.csv', sep=';')


# =============================================================================
#                            Statistiques de base
# =============================================================================

# Nb d'articles
print('%s articles' % "{:,}".format(len(df_articles)))

# Source
plt.figure(figsize = (10, 6), dpi = 80)
sns.set(style = 'darkgrid')
ax = sns.countplot(x = 'source', data = df_articles, order = df_articles['source'].value_counts().index)

# Année
years = [0]*len(df_articles)
for k in range(len(df_articles)):
    years[k] = df_articles['date'][k][6:11]
    
df_articles['year'] = years
sns.set(style = 'darkgrid')
ax = sns.countplot(x = 'year', data = df_articles)


# =============================================================================
#                             Mots les plus fréquents
# =============================================================================

# Ajouter une liste de stopwords
path = 'C:\\Users\\Etudiant\\data\\'
df_new_stops = pd.DataFrame.from_csv(path + 'new_stops.csv', sep=';')
new_stops = df_new_stops['new_stops'].values.tolist()

# Transformer la liste des contenus en dictionnaire
dict_ = []

for k in range(len(df_articles)):
    dict_.append(df_articles.loc[k]['content'])
    
dict_ = str(dict_).strip('[]')
dict_ = dict_.replace("'", "")
dict_ = dict_.split(',')

# Compter les occurrences des mots
c = Counter(dict_)


def most_common(c, type_, nb):
    if type_ == 'words':
        df = pd.DataFrame(columns = ['words', 'nb_occur'])
        
        for word, nb_occur in c.most_common(nb):
            if word not in new_stops:
                L = df.shape[0]
                df.loc[L+1] = [word, nb_occur]
     
    elif type_ == 'bigrams':
        df = pd.DataFrame(columns = ['bigrams', 'nb_occur'])
        
        for word, nb_occur in c.most_common(nb):
            if word not in new_stops:
                if '_' in word:
                    L = df.shape[0]
                    df.loc[L+1] = [word, nb_occur]
        
    return df


def plot_most_common(df, type_):
    df.plot(x = type_, y = 'nb_occur', kind = 'bar')
    

def wordcloud(df, type_):
    dict_most_common = {}
    for k in range(1, len(df)):
        dict_most_common[df.loc[k][type_]] = int(df.loc[k]['nb_occur'])
        
    most_common_cloud = WordCloud(background_color="white",
                                  width=1600,
                                  height=900).generate_from_frequencies(dict_most_common)
    plt.imshow(most_common_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

        
df_most_common_words = most_common(c, 'words', 50)
plot_most_common(df_most_common_words, 'words')
wordcloud(df_most_common_words, 'words')

df_most_common_bigrams = most_common(c, 'bigrams', 1000)
plot_most_common(df_most_common_bigrams, 'bigrams')
wordcloud(df_most_common_bigrams, 'bigrams')


# =============================================================================
#                             Topic modelling
# =============================================================================

"""
    Utilisation des mmodules de Topic Modelling de la librairie gensim
    Objectif : dégager des thèmes et mots-clés d'un corpus de textes
    Ce qui suit est largement inspiré d'un tutoriel de machinelearningplus :
    https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/?fbclid=IwAR2D9VA-3K8mRUdX0bjujEZtBeodAcyhM3p38aAtNL6SvK9UCVK7BS02b1A

"""

### 1. Mise des données au format adéquat
df = df_articles.copy()
df = df.fillna('empty')
data_token = df.content.values.tolist()
data_token = [re.sub(' ', '', w) for w in data_token]

for k in range(len(data_token)):
    if data_token[k] is not 'nan':
        data_token[k] = data_token[k].split(',')
        
data_token = [[word for word in simple_preprocess(str(doc)) if word not in new_stops] for doc in data_token]

### 2. Création d'un dictionnaire et d'un corpus
id2word = corpora.Dictionary(data_token)
texts = data_token # Create Corpus
corpus = [id2word.doc2bow(text) for text in texts]

### 3. Création du modèle "Latent Dirichlet Allocation"
def build_lda_model(nb):

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                               id2word=id2word,
                                               num_topics=nb, 
                                               random_state=100,
                                               update_every=1,
                                               chunksize=100,
                                               passes=10,
                                               alpha='auto',
                                               per_word_topics=True)
    
    doc_lda = lda_model[corpus]
    perplexity_lda = lda_model.log_perplexity(corpus)
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_token, dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    model_topics = lda_model.show_topics(formatted=False)
    
    return lda_model, doc_lda, perplexity_lda, coherence_lda, model_topics

# Générer le modèle avec 12 topcis
lda_model, doc_lda, perplexity_lda, coherence_lda, model_topics = build_lda_model(12)

### 4. Visualisation des résultats
# Visualisation des topics
pyLDAvis.enable_notebook() #si on utilise un notebook
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
pyLDAvis.show(vis)

# Trouver les topics dominants
def format_topics_sentences(ldamodel, corpus, texts):
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row[0], key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

df_topic_sents_keywords = format_topics_sentences(ldamodel = lda_model, corpus = corpus, texts = data_token)

df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_Index', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']

# Mise au bon format
df_dominant_topic_small = df_dominant_topic.copy()
del df_dominant_topic_small['Document_Index']
del df_dominant_topic_small['Topic_Perc_Contrib']
del df_dominant_topic_small['Text']

TCD = pd.pivot_table(df_dominant_topic_small,
                    index=['Dominant_Topic'],
                    aggfunc='count')

df = TCD.merge(df_dominant_topic_small, on='Dominant_Topic', how='left')
df = df.drop_duplicates()
df = df.reset_index(drop = True)
df.columns=['Dominant_Topic', 'Percentage', 'Keywords']
df['Percentage'] = 100*df['Percentage']/np.sum(df['Percentage'])
df = df.sort_values(ascending=False, by='Percentage')

# Table des topics classés par fréquence
print(df)

# Ajout des topics dominants et keywords au dataframe des articles
df_articles['Dominant_Topic'] = df_dominant_topic['Dominant_Topic']
df_articles['Keywords'] = df_dominant_topic['Keywords']

# Mots les plus fréquents et Wordcloud d'un topic
def topic_most_common(topic, nb_w, nb_b):
    dict_ = []
    
    for k in range(len(df_articles)):
        if df_articles.loc[k]['Dominant_Topic'] == topic:
            dict_.append(df_articles.loc[k]['content'])
            
    dict_ = str(dict_).strip('[]')
    dict_ = dict_.replace("'", "")
    dict_ = dict_.split(',')
    c = Counter(dict_)
    
    df_w = most_common(c, 'words', nb_w)
    df_b = most_common(c, 'bigrams', nb_b)
    
    return df_w, df_b

# Pour le topic le plus fréquent (8)
df_w_8 = topic_most_common(8, 20, 500)[0]
df_b_8 = topic_most_common(8, 20, 500)[1]

plot_most_common(df_w_8, 'words')
wordcloud(df_w_8, 'words')

plot_most_common(df_b_8, 'bigrams')
wordcloud(df_b_8, 'bigrams')


# =============================================================================
#                         Analyse des sentiments
# =============================================================================


"""
    The sentiment property returns a namedtuple of the form Sentiment(polarity, subjectivity).
    The polarity score is a float within the range [-1.0, 1.0].
    The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

"""


df_sentiment = pd.DataFrame(columns=['content','polarity', 'subjectivity', 'polarity_class', 'subjectivity_class'])
df_sentiment['content'] = df_articles['content']
df_sentiment = df_sentiment.fillna('empty')

def sentiment(df_sentiment):
    
    list_content = df_sentiment['content'].tolist()
    
    polarity = []
    subjectivity = []
    polarity_class = [0]*len(list_content)
    subjectivity_class = [0]*len(list_content)
    
    for i in range(len(list_content)):
        if list_content[i] == 'empty':
            polarity.append(0)
            subjectivity.append(0)
            
        else:
            content = list_content[i]
            blob = TextBlob(content, pos_tagger = PatternTagger(), analyzer = PatternAnalyzer())
            polarity.append(blob.sentiment[0])
            subjectivity.append(blob.sentiment[1])
            
    df_sentiment['polarity'] = polarity
    df_sentiment['subjectivity'] = subjectivity
    
    for k in range(len(df_sentiment)):
        p = df_sentiment.loc[k]['polarity']
        
        if p < - 0.05:
            polarity_class[k] = 'negative'
        
        elif p > 0.125:
            polarity_class[k] = 'positive'
            
        else:
            polarity_class[k] = 'neutral'
            
        s = df_sentiment.loc[k]['subjectivity']
        
        if s < 0.2:
            subjectivity_class[k] = 'objective'
        
        elif s > 0.5:
            subjectivity_class[k] = 'subjective'
            
        else:
            subjectivity_class[k] = 'neutral'
            
    df_sentiment['polarity_class'] = polarity_class
    df_sentiment['subjectivity_class'] = subjectivity_class
            
    return(df_sentiment)

df_sentiment = sentiment(df_sentiment)

# Ajout des sentiments au dataframe des articles
df_articles['polarity_class'] = df_sentiment['polarity_class']
df_articles['subjectivity_class'] = df_sentiment['subjectivity_class']


# =============================================================================
#                       Relation sentiments et topics
# =============================================================================

df_articles.to_csv(path + 'articles_traitements.csv', encoding='utf-8', index=True, sep=';')
    
df_relation = pd.DataFrame()
df_relation['Dominant_Topic'] = df_articles['Dominant_Topic']
df_relation['polarity_class'] = df_articles['polarity_class']
df_relation['subjectivity_class'] = df_articles['subjectivity_class']

# Tableaux croisés entre sentiments et topics
TCD_polarity = pd.pivot_table(df_relation,
                    index=['Dominant_Topic'],
                    columns=['polarity_class'],
                    aggfunc='count')

TCD_subjectivity = pd.pivot_table(df_relation,
                    index=['Dominant_Topic'],
                    columns=['subjectivity_class'],
                    aggfunc='count')

# Supprimer les topics les moins significatifs
to_del = [0, 1, 3, 5, 6, 7, 10]
TCD_polarity = TCD_polarity.drop(to_del)
TCD_subjectivity = TCD_subjectivity.drop(to_del)

# TCD en % des lignes
TCD_polarity['TOTAL'] = TCD_polarity['subjectivity_class']['negative'] + TCD_polarity['subjectivity_class']['neutral'] + TCD_polarity['subjectivity_class']['positive']
TCD_polarity = 100*TCD_polarity.div(TCD_polarity.iloc[:,-1], axis=0)

TCD_subjectivity['TOTAL'] = TCD_subjectivity['polarity_class']['objective'] + TCD_subjectivity['polarity_class']['neutral'] + TCD_subjectivity['polarity_class']['subjective']
TCD_subjectivity = 100*TCD_subjectivity.div(TCD_subjectivity.iloc[:,-1], axis=0)

# Le topic 9 (monde, coupe, qatar, football, mondial, pays, hiver, jouer, decembre, rugby)
# est moins neutre : il est considéré comme + subjectif et avec des opinions + négatives ou positives


# =============================================================================
#                Analyse des articles sur Blatter et Platini
# =============================================================================

df_articles_persons = pd.DataFrame.from_csv(path + 'articles_persons_trait.csv', sep=';')

list_blatter = [0]*len(df_articles)
list_platini = [0]*len(df_articles)

for k in range(len(df_articles_persons)):
    pers = df_articles_persons.loc[k]['id_pers']
    art = df_articles_persons.loc[k]['id_article']
    
    if pers == 148:
        list_blatter[art] = 1
    
    if pers == 204:
        list_platini[art] = 1    
     
        
df_articles['concerne_blatter'] = list_blatter
df_articles['concerne_platini'] = list_platini

somme_list = [list_blatter[i] + list_platini[i] for i in range(len(list_blatter))]
dict([(k, somme_list.count(k)) for k in set(somme_list)])

# 327 articles concernent à la fois Blatter et Platini, 551 concernent 1 des 2

# Polarité
# TCD Excel : rien de significatif

# Mots les plus fréquents et Wordcloud concernant une personne
def pers_most_common(concerne_nom, nb_w, nb_b):
    dict_ = []
    
    for k in range(len(df_articles)):
        if df_articles.loc[k][concerne_nom] == 1:
            dict_.append(df_articles.loc[k]['content'])
            
    dict_ = str(dict_).strip('[]')
    dict_ = dict_.replace("'", "")
    dict_ = dict_.split(',')
    c = Counter(dict_)
    
    df_w = most_common(c, 'words', nb_w)
    df_b = most_common(c, 'bigrams', nb_b)
    
    return df_w, df_b

# Pour le topic le plus fréquent (8)
df_w_blatter = pers_most_common('concerne_blatter', 15, 200)[0]
df_b_blatter = pers_most_common('concerne_blatter', 15, 200)[1]

plot_most_common(df_b_blatter, 'bigrams') # le seul pertinent


# =============================================================================
#               Analyse des articles de Courrier International
# =============================================================================

# même niveau de neutralité polarity (70%) et subjectivity (40%) que l'ensemble

df_articles_countries = pd.DataFrame.from_csv(path + '\\POUR_BD\\articles_countries.csv', sep=';')
df_countries = pd.DataFrame.from_csv(path + '\\POUR_BD\\countries_list.csv', sep=';')

countries_a = [0]*len(df_articles_countries)

for k in range(len(df_articles_countries)):
    countries_a[k] = df_countries.loc[df_articles_countries.loc[k]['id_country']]['country']

df_articles['country'] = countries_a
df_courrierint = df_articles.loc[:53] 
to_del = ['source', 'url', 'date', 'theme', 'title', 'subtitle', 'content', 'abo', 'content_type', 'Dominant_Topic', 'Keywords', 'concerne_blatter', 'concerne_platini']
df_courrierint = df_courrierint.drop(to_del, axis=1)
        
plt.figure(figsize = (10, 6), dpi = 80)
sns.set(style = 'darkgrid')
ax = sns.countplot(x = 'country', data = df_courrierint, order = df_courrierint['country'].value_counts().index)

to_keep = ['France', 'Qatar', 'Royaume-Uni']
id_to_keep = []

for k in range(len(df_courrierint)):
    if df_courrierint.loc[k]['country'] not in to_keep:
        df_courrierint = df_courrierint.drop(k)
    
pd.pivot_table(df_courrierint,
               index=['country'],
               columns=['polarity_class'],
               aggfunc='count')

# Qatar : 8 articles dont aucun négatif, 4 positifs et 4 neutres
# RU : 16 articles dont 10 neutres, 4 positifs, 2 négatifs
# France : 8 articles dont aucun négatif, 2 positifs et 4 neutres
       
pd.pivot_table(df_courrierint,
               index=['country'],
               columns=['subjectivity_class'],
               aggfunc='count')

# Qatar : 8 articles dont aucun subjectif, 4 objectifs et 4 neutres
# RU : 16 articles dont 6 neutres, 6 objectifs, 4 subjectifs
# France : 8 articles dont aucun neutre, 5 objectifs et 1 subjectif    
