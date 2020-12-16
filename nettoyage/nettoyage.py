# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 16:11:08 2019

"""


from nltk.corpus import stopwords
import pandas as pd
import os
import datetime
import re
import gensim
from gensim.utils import simple_preprocess
import spacy
import nltk

# Stopwords
nltk.download('stopwords')
stop_words = stopwords.words('french')
df_addstops = pd.DataFrame.from_csv(
    os.path.join(os.path.abspath('..'), 'data', 'add_stops.csv'), sep=';')
to_add = df_addstops['add_stops'].values.tolist()
to_add = [re.sub(' ', '', word) for word in to_add]
stop_words.extend(to_add)
stop_words.sort()


# =============================================================================
#                            Tokenisation et nettoyage
# =============================================================================


def basic_cleaner(data):
    in_ = ["\'", '\s+', 'é', 'è', 'ë', 'ê', 'à', 'â', 'ä', 'î', 'ï', 'ô', 'ö', 'œ', 'æ', 'û', 'ü', 'ù', 'ú', 'ç', 'À', 'Â', 'É', 'È', 'Ê', 'Ë', 'Î', 'Ï', 'Ô', 'Ö', 'Ù', 'Û', 'Ü', 'Ç', 'Œ', 'Æ', 'Ã©', 'Ã¨', 'Ã¯', 'Ã´',
           'Ã§', 'Ãª', 'Ã¹', 'Ã¦', 'Å', 'Ã«', 'Ã¼', 'Ã¢', 'â¬', 'Â©', 'Ã', 'Ã®', 'Ã¶', 'Ã»', 'Å', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Å', '\t', '\n', '\x92', '-', '/', 'Ãº']

    out_ = ['', ' ', 'e', 'e', 'e', 'e', 'a', 'a', 'a', 'i', 'i', 'o', 'o', 'oe', 'ae', 'u', 'u', 'u', 'u', 'c', 'a', 'a', 'e', 'e', 'e', 'e', 'i', 'i', 'o', 'o', 'u', 'u', 'u', 'c', 'oe', 'ae', 'e',
            'e', 'i', 'o', 'c', 'e', 'u', 'ae', 'oe', 'e', 'u', 'a', 'e', 'c', 'a', 'i', 'o', 'u', 'oe', 'A', 'A', 'E', 'E', 'E', 'E', 'I', 'I', 'O', 'O', 'U', 'U', 'U', 'C', 'OE', '', '', '', '', '', 'u']

    for j in range(len(in_)):
        data = [re.sub(in_[j], out_[j], sent) for sent in data]

    return data


# Tokenisation de chaque phrase en une liste de mots, en retirant la ponctuation et les caractères superflus
def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True retire la punctuation
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))


def clean_date(df):
    for i in range(len(df)):
        df.date[i] = str(df.date[i])[:10]


def clean_theme(df):
    for i in range(len(df)):
        theme = df.theme[i]
        in_ = ['é', 'è', 'ë', 'ê', 'à', 'â', 'ä', 'î', 'ï', 'ô', 'ö', 'œ', 'æ', 'û', 'ü', 'ù', 'ú', 'ç', 'À', 'Â', 'É', 'È', 'Ê', 'Ë', 'Î', 'Ï', 'Ô', 'Ö', 'Ù', 'Û', 'Ü', 'Ç', 'Œ', 'Æ', 'Ã©', 'Ã¨', 'Ã¯', 'Ã´', 'Ã§', 'Ãª', 'Ã¹',
               'Ã¦', 'Å', 'Ã«', 'Ã¼', 'Ã¢', 'â¬', 'Â©', 'Ã', 'Ã®', 'Ã¶', 'Ã»', 'Å', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Ã', 'Å', '\t', '\n', '\x92', '-', '(', ')', '.', '/', '?', '!', 'Ãº']

        out_ = ['e', 'e', 'e', 'e', 'a', 'a', 'a', 'i', 'i', 'o', 'o', 'oe', 'ae', 'u', 'u', 'u', 'u', 'c', 'a', 'a', 'e', 'e', 'e', 'e', 'i', 'i', 'o', 'o', 'u', 'u', 'u', 'c', 'oe', 'ae', 'e', 'e', 'i', 'o',
                'c', 'e', 'u', 'ae', 'oe', 'e', 'u', 'a', 'e', 'c', 'a', 'i', 'o', 'u', 'oe', 'A', 'A', 'E', 'E', 'E', 'E', 'I', 'I', 'O', 'O', 'U', 'U', 'U', 'C', 'OE', '', '', '', '', '', '', '', '', '', '', 'u']

        for j in range(len(in_)):
            theme = theme.replace(in_[j], out_[j])
        theme = theme.lower()
        theme.strip(' ')
        theme = theme.split(',')
        if df.source[i] == 'football365':
            del theme[-1]
        del theme[-1]
        theme = basic_cleaner(theme)
        theme = str(theme).strip('[]')
        theme = theme.replace("'", '')
        df.theme[i] = theme


# =============================================================================
#             Création du modèle Bigrams, suppression des stopwords,
#                     remplacement des bigrams, lemmatisation
# =============================================================================


def bigram(data_words):
    # seuil = grand <=> moins de phrases
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return(bigram_mod)


def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]


def make_bigrams(texts, bigram_mod):
    return [bigram_mod[doc] for doc in texts]


# =============================================================================
#                          Exécution des fonctions
# =============================================================================


def clean_tokenize(data):
    data = basic_cleaner(data)
    data_words = list(sent_to_words(data))
    bigram_mod = bigram(data_words)
    data_words_nostops = remove_stopwords(data_words)
    data_words_bigrams = make_bigrams(data_words_nostops, bigram_mod)
    return data_words_bigrams


def lists_to_strings(list_):
    for i in range(len(list_)):
        list_[i] = str(list_[i]).strip('[]')
    return list_


df_list = []

filenames = os.listdir(os.path.join(os.path.abspath('..'), 'data'))
filenames = [x for x in filenames if '.json' in x]
nb_files = len(filenames)

for f in filenames:
    df = pd.read_json(f)
    df_list.append(df)

df_all = pd.concat(df_list)
df_all.reset_index(drop=True, inplace=True)

clean_date(df_all)
clean_theme(df_all)

data = df_all.title.values.tolist()
title_data_words_bigrams = lists_to_strings(clean_tokenize(data))

data = df_all.subtitle.values.tolist()
subtitle_data_words_bigrams = lists_to_strings(clean_tokenize(data))

data = df_all.content.values.tolist()
content_data_words_bigrams = lists_to_strings(clean_tokenize(data))


# =============================================================================
#                            Liste des bigrams
# =============================================================================


bigrams_list = []

full_list = title_data_words_bigrams + \
    subtitle_data_words_bigrams + content_data_words_bigrams

for k in range(len(full_list)):
    for j in range(len(full_list[k])):
        if '_' in full_list[k][j]:
            bigrams_list.append(full_list[k][j])

bigrams_list = list(dict.fromkeys(bigrams_list))


# =============================================================================
#                  Traitement des bigrams personnes et stades
# =============================================================================


df_stadiums = pd.DataFrame.from_csv(
    os.path.join(os.path.abspath('..'), 'data', 'stadiums.csv'), sep=';')
df_persons = pd.DataFrame.from_csv(
    os.path.join(os.path.abspath('..'), 'data', 'persons.csv'), sep=';')

stades_in = df_stadiums['stades_in'].tolist()
stades_out = df_stadiums['stades_out'].tolist()
liste_in = df_persons['liste_in'].tolist()
liste_out = df_persons['liste_out'].tolist()


def replace_bigrams(data):
    for i in range(len(stades_in)):
        data = [re.sub(stades_in[i], stades_out[i], sent) for sent in data]

    for j in range(len(liste_in)):
        data = [re.sub(liste_in[j], liste_out[j], sent) for sent in data]
    return data


title_data_words_bigrams = replace_bigrams(title_data_words_bigrams)
subtitle_data_words_bigrams = replace_bigrams(subtitle_data_words_bigrams)
content_data_words_bigrams = replace_bigrams(content_data_words_bigrams)

df_persons = pd.DataFrame.from_csv(
    os.path.join(os.path.abspath('..'), 'data', 'persons_list.csv'), sep=';')
persons_list = df_persons['pers'].tolist()
df_articles_persons = pd.DataFrame(columns=['id_article', 'id_pers'])

df_stadiums = pd.DataFrame.from_csv(
    os.path.join(os.path.abspath('..'), 'data', 'stadiums_list.csv'), sep=';')
stadiums_list = df_stadiums['stades_out'].tolist()
df_articles_stadiums = pd.DataFrame(columns=['id_article', 'id_stadium'])

types = ['title_data_words_bigrams',
         'subtitle_data_words_bigrams', 'content_data_words_bigrams']

for k in range(len(content_data_words_bigrams)):
    for i in range(len(persons_list)):
        if persons_list[i] in content_data_words_bigrams[k]:
            L = df_articles_persons.shape[0]
            df_articles_persons.loc[L+1] = [k, i]

for k in range(len(content_data_words_bigrams)):
    for i in range(len(stadiums_list)):
        if stadiums_list[i] in content_data_words_bigrams[k]:
            L = df_articles_stadiums.shape[0]
            df_articles_stadiums.loc[L+1] = [k, i]

title_data_words_bigrams = [re.sub("'", "", i)
                            for i in title_data_words_bigrams]
subtitle_data_words_bigrams = [re.sub("'", "", i)
                               for i in subtitle_data_words_bigrams]
content_data_words_bigrams = [re.sub("'", "", i)
                              for i in content_data_words_bigrams]


# =============================================================================
#                            Sauvegarde en csv
# =============================================================================


if __name__ == '__main__':

    df_all['title'] = title_data_words_bigrams
    df_all['subtitle'] = subtitle_data_words_bigrams
    df_all['content'] = content_data_words_bigrams

    now = datetime.datetime.now().isoformat()
    filename = f'{now[:10]}_articles_clean.csv'
    df_all.to_csv(os.path.join(os.path.abspath('..'), 'data',
                               filename), encoding='utf-8', index=True, sep=';')
    df_articles_persons.to_csv(os.path.join(os.path.abspath(
        '..'), 'data', 'articles_persons.csv'), encoding='utf-8', index=True, sep=';')
    df_articles_stadiums.to_csv(os.path.join(os.path.abspath(
        '..'), 'data', 'articles_stadiums.csv'), encoding='utf-8', index=True, sep=';')
    
    