# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 16:08:52 2019

"""

import json

path = 'C:\\Users\\egran\\data\\'
filename = '2019-02-20_all_articles_courrierint.json'
f = open(path + filename, encoding='utf-8')
doc = json.load(f)
