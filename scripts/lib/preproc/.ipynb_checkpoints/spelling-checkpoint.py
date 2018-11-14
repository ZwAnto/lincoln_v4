from ..other.progress import *

import enchant
from nltk.metrics import edit_distance
import numpy as np

class SpellingReplacer(object):
    def __init__(self, dict_name = 'fr_FR', max_dist = 2):
        self.spell_dict = enchant.Dict(dict_name)
        
        self.max_dist = max_dist
        self.actions = []
        
    def replace(self, l):
        
        pBar = progress(len(l),50)
        step = 1
        
        out = []
        for k in l:
            
            correct = []
            for word in k:                
                if self.spell_dict.check(word):
                    correct.append(word)
                    continue
                else:
                    continue
                
                suggestions = self.spell_dict.suggest(word)

                if suggestions:
                    dist = [edit_distance(word, i) for i in suggestions]
                    idx = np.argmin(dist)

                    if dist[idx] <= self.max_dist:
                        correct.append(suggestions[idx])
                        self.actions.append([word,suggestions[idx]])
                    else:
                        #correct.append(word)
                        continue
                else:
                    #correct.append(word)
                    continue
            
            out.append(correct) 
            if step % 10 == 0 or step == (len(l)):
                pBar.show(step)
            step +=1
            
        return(out)