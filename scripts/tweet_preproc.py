from lib.data.import_json import import_json
from lib.preproc.tokenizer import tweet_tokenzier
from lib.preproc.spelling import SpellingReplacer
from lib.preproc.tag import treeTagger
from lib.other.saveload import *

import re

import numpy as np
import pandas as pd
import datetime as dt

from nltk.tokenize import word_tokenize

# DATA ############################################################

tweets = import_json(sample = False, full = True)

# NAMES ###########################################################

names = []
for tweet in tweets:
    if tweet['entities']['user_mentions']:
        for user in tweet['entities']['user_mentions']:
            if not user['screen_name'] in names:
                names.append(user['screen_name'])

for tweet in tweets:
    names.append(tweet['user']['screen_name'])

                
names += [re.sub('_','',i) for i in names]
names += [re.sub('_',' ',i) for i in names]  
names = list(set(names))   
names = [i.strip() for i in names]

# TOKEN ###########################################################

tokenizer = tweet_tokenzier()
tweets_text = tokenizer.tokenize_list([i['text'] for i in tweets])

# SPELLCHECK ######################################################

checker = SpellingReplacer()
tweets_text = checker.replace(tweets_text)
checker.actions

# POS TAGGING ####################################################

tagger = treeTagger()
tweets_text, tweets_type = tagger.tag(tweets_text)

tweets_text = [word_tokenize(i) for i in tweets_text]

# LOWCASE ########################################################

for i in range(len(tweets_text)):
    for j in range(len(tweets_text[i])):
        tweets_text[i][j] = tweets_text[i][j].lower()

# STOP WORDS #####################################################

import nltk
stopWords = nltk.corpus.stopwords.words('french')

for i in range(len(tweets_text)):
    words_filtered = []
    for w in tweets_text[i]:
        if w not in stopWords:
            words_filtered.append(w)
    tweets_text[i] = words_filtered

pd.DataFrame({'r':tweets_text})
    
save(tweets_text,'../data/tweets_clean.pkl')
