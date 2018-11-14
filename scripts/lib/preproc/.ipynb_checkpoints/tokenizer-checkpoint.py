import numpy as np
from nltk.tokenize import TweetTokenizer, word_tokenize, wordpunct_tokenize
from nltk.tokenize.casual import TweetTokenizer
import re
import nltk
nltk.download('stopwords')

stopWords = nltk.corpus.stopwords.words('french')

class tweet_tokenzier:
    
    def __init__(self):
        self.tokenizer = TweetTokenizer(preserve_case=True,reduce_len=False)
            
    def tokenize(self,string,keep_punct = False, keep_url = False, keep_tweetSlang = False):
        
        if not keep_url:
            string = re.sub(pattern=r'http\S+',repl='',string=string)
        if not keep_punct:
            string = re.sub(pattern=r'[?,;:.]',repl='',string=string)
        string = re.sub(pattern=r'  ',repl=' ',string=string)
        if not keep_tweetSlang:
            string = re.sub(pattern=r'RT|[#]',repl=' ',string=string)
            string = re.sub(pattern=r'@\S+',repl='',string=string)
    
        #string = re.sub(pattern=r'jo|202[48]',repl=' ',string=string, flags=re.IGNORECASE)
        string = re.sub(pattern=r'^\s*[:,.;]',repl=' ',string=string, flags=re.IGNORECASE)
        string = re.sub(pattern=r'[-\'\"\(\)«»]',repl=' ',string=string, flags=re.IGNORECASE)
        string = re.sub(pattern='[0-9]{2}(/|-)[0-9]{2}(/|-)[0-9]{4}',repl='',string=string)
        string = re.sub(pattern='[0-9]{4}(/|-)[0-9]{2}(/|-)[0-9]{2}',repl='',string=string)
        #string = re.sub(pattern=r'@\S+',repl='',string=string)
        
        string = self.tokenizer.tokenize(string)
        #wordsFiltered = []
        #for w in string:
        #    if w not in stopWords:
        #        wordsFiltered.append(w)
    
        return(string)
    
    def tokenize_list(self,string_list,keep_punct = False, keep_url = False, keep_tweetSlang = False):
        string_list = [self.tokenize(string = string,
                                            keep_punct = keep_punct,
                                            keep_url = keep_url,
                                            keep_tweetSlang = keep_tweetSlang) for string in string_list]
    
        return(string_list)

'''
tokenizer = tweet_tokenzier()
tokens = tokenizer.tokenize_list(tweet)


import enchant
test = enchant.Dict('fr_FR')

not_word = []
for token in tokens:
    for w in token:
        if not test.check(w):
            if len(not_word) == 0:
                not_word.append(w)
            else:
                if not w in not_word:
                    not_word.append(w)
            

not_word
'''