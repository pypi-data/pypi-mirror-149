import pickle

def pickle_save(filename, object_name):
    with open(filename, 'wb') as f:
        pickle.dump(object_name, f)

def pickle_load(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
