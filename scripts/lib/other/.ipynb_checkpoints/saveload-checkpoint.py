import pickle

def load(path):
    with open(path, 'rb') as handle:
        obj = pickle.load(handle)
    return(obj)

def save(obj,path):
    with open(path, 'wb') as handle:
        pickle.dump(obj,handle,protocol=pickle.HIGHEST_PROTOCOL)
    return