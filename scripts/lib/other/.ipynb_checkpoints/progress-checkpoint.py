import math, sys, time

class progress:
    
    def __init__(self,max,size):
        self.time = time.time()
        self.max = max
        self.size = size

    def show(self,actual):
        
        timeActual = time.time()
        
        r = self.max/self.size

        n = math.floor(actual/r)

        pct = round(actual/r/self.size*100,2)

        text = '\r[\033[92m' + '='*(n-1) + '>' + ' '*(self.size-n) + '\033[0m] ' + str(actual) + '/' + str(self.max) + ' ' + str(pct) + '% '
        
        t = (timeActual - self.time)/actual*(self.max-actual)
        if t>3600:
            text += str(round(t/3600,2)) + 'h'
        elif t>60:
            text += str(round(t/60,2)) + 'm'
        else:
            text += str(round(t,2)) + 's'

        sys.stdout.write(text)
        sys.stdout.flush()
        
        return