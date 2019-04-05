'''Jaccard Similarity (String similarity)
'''
from jaccard_index.jaccard import jaccard_index

def compare(original, archived):
    return (jaccard_index(original.read(), archived.read()), None)
