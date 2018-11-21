#!/usr/bin/env python3

"""
Merge JSON schema specifications.

Schema of each entity is represented as a tree;
common keys occur only once, and keys specific
to certain schemas are added as an "optional edge".

Edges can have attributes which can carry information
(such as being optional, type of the subtree/entity, etc.)
"""

import json
import collections
from functools import reduce
import pickle
from trie import Trie
import nltk

class JSONSchema:
    """ Wrapper class to handle working with JSON schema files. """
    def __init__(self, file):
        self.file = file
        try:
            self.file_handle = open(self.file, 'r')
            self.data = json.load( self.file_handle )
        except Exception:
            print( f"Error: Couldn't load schema from '{self.file}'" )
    
    def __getitem__(self, key):
        try:
            return self.data[key]
        except Exception:
            print( f"Error: Couldn't fetch key '{key}' from '{self.file}' ")
            raise SystemExit
    
    def __del__(self):
        if self.file_handle:
            try:
                self.file_handle.close()
            except:
                print( f"Error closing handle to file '{self.file}' ")

class TreeNode:
    def __init__(self):
        self.edges = {}
        self.__count = 0
    def addChild(self, keyName):
        keyName = keyName.lower()
        if (keyName in self.edges):
            self.edges[keyName]['times'] += 1
            return
        self.edges[keyName] = {}
        self.edges[keyName]['id'] = self.__count
        self.edges[keyName]['times'] = 1
        self.__count += 1
    def getFrequencies(self):
        freq = collections.defaultdict(list)
        maxfreq = None
        for key in self.edges:
            f = self.edges[key]['times']
            freq[ f ].append(key)
            if (maxfreq == None) or (f > maxfreq):
                maxfreq = f
        merged, optional = [], []
        for key in self.edges:
            f = self.edges[key]['times']
            if f == maxfreq:
                merged.append(key)
            else:
                optional.append(key)
        print( "List of merged keys: " )
        print( ', '.join(merged) )
        print( "List of optional keys: " )
        print( ', '.join(optional) )


userwords = None
with open('pickled_userwords', 'rb') as f:
    userwords = pickle.load(f)

def split_into_chunks(word):
    if not word:
        return []
    word = word.lower()
    res = []

    Sources = []
    for Len in reversed(range(3, len(word)+1)):
        for start in range(0, len(word)):
            end = start + Len
            if end > len(word):
                break
            bef, chunk, after = word[:start], word[start:end], word[end:]
            if userwords.find(chunk, prefix_match=1):
                if bef:
                    r1 = split_into_chunks(bef)
                    for w in r1:
                        res.append(w)
                res.append(chunk)
                if after:
                    r2 = split_into_chunks(after)
                    for w in r2:
                        res.append(w)
                return res
    return [word]

def chunk_similarity(a,b):
    chunked_a, chunked_b = split_into_chunks(a), split_into_chunks(b)
    print()
    print(f"Matching: '{a}' with '{b}'")
    print(f'{a} -> {chunked_a}')
    print(f'{b} -> {chunked_b}')
    unmatched = set(range(len(chunked_a)))
    unmatched_b = set(range(len(chunked_b)))
    matches = []
    char_match = 0
    for i in unmatched:
        pq = []
        for j in unmatched_b:
            pq.append( (nltk.edit_distance(chunked_a[i], chunked_b[j]), j) )
        pq = sorted(pq)
        if not pq:
            continue
        best = pq[0][1]
        best_match = chunked_b[best]
        matches.append( (chunked_a[i], best_match) )
        unmatched_b.remove(j)
    for row in matches:
        print(row)
    return matches

def match_names(a, b):
    """
    Takes lists of names (key names) and matches
    them based on their similarity. Returns a list of
    tuples, where (p, u, v) means name u and name v
    are assumed to be similar with a probability of p

    Matching proceeds in phases:
        1. Exact matching - If a name in list A exactly
        matches a name from list B, they are matched together
        and dropped from consideration for future phases.

        2. Chunk similarity - Each name in listA is chunked into
        pieces using an English dictionary and terms from user stories.
        When comparing the chunked name pairs, edit distance similarity is used.
    """
    Res = []

    """ exact """
    def exact_match(a,b):
        Res = []
        _a = [ (x.lower(), x) for x in a ]
        _b = [ (x.lower(), x) for x in b ]
        _matched_a, _matched_b = set(), set()
        for i, name1 in enumerate(_a):
            if i in _matched_a:
                continue
            for j, name2 in enumerate(_b):
                if j in _matched_b:
                    continue
                if name1[0] == name2[0]:
                    Res.append( ('exact', 1.0, name1[1], name2[1]) )
                    _matched_a.add(i)
                    _matched_b.add(j)
        a = list(map(lambda i: a[i], set(range(len(a))) - _matched_a))
        b = list(map(lambda i: b[i], set(range(len(b))) - _matched_b))
        return (Res, a, b)
    exact_matches, a, b = exact_match(a,b)
    print('Exact matches: ')
    for row in exact_matches:
        print(row)

    """ chunk matching """


    
    print('Remaining: ')
    print(a)
    print(b)
    return



if __name__ == "__main__":
    a = ['fname', 'lname', 'firstname']
    b = ['FName', 'lastname', 'cameraMetadata']
    match_names(a,b)

    print()
    print( 'Testing chunking...' )
    # pickle file must be regenerated if new words added
    print( split_into_chunks('camerametadata') )
    print( split_into_chunks('datfromCam') )
    print( split_into_chunks('username') )
    print( split_into_chunks('deptName') )
    print( split_into_chunks('department') )
    print( split_into_chunks('apartment') )
    print( split_into_chunks('uploadDate') )
    print( split_into_chunks('vehicleDescription') )
    print( split_into_chunks('vehicleDescripton') )

    chunk_similarity( 'vehicleDescription', 'vehicleDescripton' )



    """
    test = JSONSchema('mongo.txt')
    for document in test['1']['entities']:
        root = TreeNode()
        print( f'Schema for {document}:' )
        for List in test['1']['entities'][document]:
            for key in List:
                root.addChild(key)
        root.getFrequencies()
        print()
    """
