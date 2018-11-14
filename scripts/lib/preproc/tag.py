
import treetaggerwrapper
import re

class treeTagger:
     
    def __init__(self):
        self.tagger =  treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='/opt/treetagger/',TAGPARFILE='/opt/treetagger/lib/french.par')

        
    def tag(self,tweets):
        out = []
        outtype = []
        for tweet in tweets:
            tags = ''
            tagstype = []
            for tag in self.tagger.TagText(tweet):
                origin = tag.split('\t')[0]
                lem = tag.split('\t')[2]
                tagtype = tag.split('\t')[1]
                if re.match('^(ADJ|ADV|NAM|NOM|NUM|VER)',tagtype) and not re.match('être|avoir|etre',lem):
                    tagstype.append(tagtype)
                    if re.match('[0-9]+',origin):
                        tags += ' ' + origin
                    else:
                        tags += ' ' + lem
            out.append(tags.strip())
            outtype.append(tagstype)

        return((out,outtype))
