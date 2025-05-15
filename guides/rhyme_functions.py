import string
from collections import defaultdict
from functools import reduce
from itertools import chain

# helper functions for transitive closure
# based on https://stackoverflow.com/questions/69666329/transitive-closure

def connect(D, k):
    connects_to = D[k]
    for v in connects_to:
        connects_to = connects_to + connect(D,v)
    return connects_to

def closure(D):
    closure = dict()
    for k in D.keys():
        closure[k] = connect(D,k)
    return closure

# user functions

def distances_to_pairs(distances):
    '''converts a distance scheme to a dictionary graph of connected line pairs'''
    pairs = dict()
    for idx, d in enumerate(distances):    
        if d != 0:
            pairs[idx] = [idx+d]
        else:
            pairs[idx] = []
    return pairs

def distances_to_ab(distances):
    '''converts a distance rhyme scheme (list of ints) into an AB-style rhyme scheme'''
    ABCs = string.ascii_uppercase
    pairs = dict()
    groups = dict()
    scheme_dict = dict()
    
    # convert distances to graph
    for idx, d in enumerate(distances):    
        if d != 0:
            pairs[idx] = [idx+d]
        else:
            pairs[idx] = []
    
    # get transitive closure of graph
    graph = closure(pairs)                  
    
    # assign an AB-scheme letter to all connected components
    # can safely handle linegroups that need more than 26 letters
    i = 0
    for k in sorted(list(graph.keys())):
        if k not in list(chain.from_iterable(groups.values())):
            if i >= 26:
                abc_idx = i % 26
                suffix = str(i // 26)
            else:
                abc_idx = i
                suffix = ''
            groups[ABCs[abc_idx] + suffix] = [k] + graph[k]
            i += 1
    for group, lines in groups.items():
        for line in lines:
            scheme_dict[line] = group
    scheme = sorted(list(scheme_dict.items()))

    return ''.join([ab for _, ab in scheme])

def get_oneoffs(distances):
    '''given a distance scheme as a list, returns a list of all oneoffs and the line pair that differs'''
    oneoffs = dict()
    rhyme_idx = [idx for idx,d in enumerate(distances) if int(d) > 0]
    for idx in rhyme_idx:
        oneoff = distances[:idx] + [0] + distances[idx+1:]
        lines = (idx+1, idx+distances[idx]+1)
        oneoffs[lines] = oneoff
    return oneoffs