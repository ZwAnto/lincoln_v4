
from lib.other.saveload import *
from lib.data.import_json import import_json

import json

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.cluster import DBSCAN
from time import sleep
from collections import Counter

# DATA ###########################################################

tweets_text = load('../data/tweets_clean.pkl')
tweets = import_json(sample = False, full = True)

# DICTIONNARY ####################################################

dictionnary = []
for tweet in tweets_text:
    for w in tweet:
            dictionnary.append(w)
            
dictionnary = pd.DataFrame(dictionnary)
dictionnary.columns = ['word']
dictionnary = dictionnary.groupby('word').size().reset_index(name='counts')
dictionnary = dictionnary.sort_values(ascending=False,by='counts')

dictionnary = dictionnary[dictionnary.counts > 11]

# BOW ############################################################

df = pd.DataFrame({'text':tweets_text})

L = dictionnary.word.values

f = lambda x: Counter([y for y in x if y in L])
bow = pd.DataFrame((pd.DataFrame(df['text'].apply(f).values.tolist())
               .fillna(0)
               .astype(int)
               .reindex(columns=L)
               .values))
bow.columns = L

# DATE ###########################################################

date_fmt = '%a %b %d %H:%M:%S %z %Y'

datetime = [dt.datetime.strptime(i['created_at'], date_fmt) for i in tweets]
date = [dt.datetime.strptime(i['created_at'], date_fmt).date() for i in tweets]
date_monday = [(i - dt.timedelta(days=i.weekday())).isoformat() for i in date]
month = [dt.datetime.strptime(i['created_at'], date_fmt).strftime('%m-%Y') for i in tweets]

bow['filter_datetime'] = date
bow['filter_date'] = date
bow['filter_week'] = date_monday
bow['filter_month'] = month

# TF IDF #########################################################

bow_agg = bow.groupby('filter_week').sum()

rolling_agg = bow_agg.rolling(5, center = True, min_periods = 1).sum()

tf = rolling_agg.div(rolling_agg.sum(axis=1),axis=0)
idf = np.log(len(bow_agg) /  bow_agg.astype(bool).sum(axis=0))
tf_idf = tf.multiply(idf)

tf_idf = tf_idf.fillna(0,axis=1)

# CLUSTERING #####################################################

# TSNE
tsne = TSNE(n_components=2,
            random_state= 1121993)
x_tsne = tsne.fit_transform(tf_idf)

# DBSCAN
dbscan = DBSCAN(eps=2, min_samples=1)
labels = dbscan.fit(x_tsne).labels_

# PLOTING TSNE
fig,ax = plt.subplots(figsize=[8,5])
ax.scatter(x_tsne[:,0],x_tsne[:,1],c=labels)
for i in set(labels):
    x,y = np.mean(x_tsne[labels == i],axis = 0)
    ax.text(x,y,s = i)
fig.patch.set_facecolor((250/255,250/255,250/255))
plt.savefig('../img/tsne.png',facecolor=fig.get_facecolor())

# PLOTING GROUP VS WEEK
fig,ax = plt.subplots(figsize=[8,5])
ax.scatter(bow_agg.index.values.astype('datetime64'),
            labels,
            c = labels)
fig.patch.set_facecolor((250/255,250/255,250/255))
plt.savefig('../img/hebdo.png',facecolor=fig.get_facecolor())

# DATA FOR HIGHCHART GRAPH #######################################

bow_agg['filter_group'] = labels 
tf_idf['filter_group'] = labels 

bow_agg['filter_week'] = bow_agg.index.values

# Word density of each group
worddensity = tf_idf.groupby('filter_group').sum()

# Date range of each gorup
date_min = bow_agg.groupby('filter_group')['filter_week'].agg(min)
date_max = bow_agg.groupby('filter_group')['filter_week'].agg(max)

# Number of tweet in each group
count = bow.groupby('filter_week').size().reset_index(name='counts')

color = ['#1B95E0','#84d0ff']

series = []
for i in range(len(date_min)):
    if (i == len(date_min)-1):
        count_i = np.asarray(count[(count['filter_week'] >= date_min[i]) & (count['filter_week'] <= date_max[i])])
    else:
        count_i = np.asarray(count[(count['filter_week'] >= date_min[i]) & (count['filter_week'] <= date_min[i+1])])
    out=[]
    for j in count_i:
        text = '["' + str(j[0]) + '",' + str(j[1])  + ']'
        out.append(text)
    out = ','.join(out)
    series.append('{"name": "' + str(i) + '", "color": "' + color[i % 2] + '" ,' + '"data": [' + out + ']}')
    
series = '[' + ','.join(series) + ']'

save(series,'../data/data.json')

# 10 BEST WORD FOR EACH GROUP ####################################

nlargest = 10
order = np.argsort(-worddensity.values, axis=1)[:, :nlargest]
result = pd.DataFrame(worddensity.columns[order], 
                      columns=['top{}'.format(i) for i in range(1, nlargest+1)],
                      index=worddensity.index)

result['date_min'] = date_min
result['date_max'] = date_max

out=[]
for i in range(len(result)):
    out.append('{"group": "' + str(i) + '","date_min" : "' + str(result.iloc[i,10]) + '", "date_max" : "' + str(result.iloc[i,11]) + '", "text" : "' + " ".join(result.iloc[i,:10]) + '"}')
out = '[' + ','.join(out) + ']'

save(out,'../data/group.json')

# ELASTIC INDEXING ###############################################

ids = [i['id'] for i in tweets]
partial_text = [' '.join(set(i)) for i in tweets_text]
partial_text = pd.DataFrame({'text': partial_text, 'date': date},index=ids)
partial_text = partial_text.drop_duplicates(subset='text')

from elasticsearch import Elasticsearch
es = Elasticsearch(hosts='xxxxxxx:80')

actions = []
for i in range(partial_text.shape[0]):    
    actions.append({'index': {'_index' : 'lincoln_v4_partial_v1','_type' : '_doc','_id' : int(partial_text.index[i]) }})
    actions.append({
        'date': str(partial_text.iloc[i,0]),
        'text': partial_text.iloc[i,1]
    })
es.bulk(actions, index = 'lincoln_v4_partial_v1')

# WORDCLOUD ######################################################

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import random

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(%d, 100%%, 50%%)" % (random.randint(190, 210))

for k in range(len(worddensity)):
    a = worddensity.iloc[k]
    a = a[a.values>0] * 1000
    text = ''
    for i in range(len(a)):
        for n in range(int(a.values[i])):
            text += ' ' + a.index[i]

    mask = np.array(Image.open("../img/twitter_mask.png"))
    wordcloud = WordCloud(collocations=False,mask=mask,max_words=100,
                          relative_scaling=0.5,
                          background_color='white').generate(text)

    # create coloring from image

    plt.figure(figsize=[15,15])
    
    fig = plt.imshow(wordcloud.recolor(color_func=grey_color_func), interpolation='bilinear')
    fig.axes.axis('off')
    plt.savefig('../img/' + str(k) + '.png')
