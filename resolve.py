#!/usr/bin/env/python3

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



if __name__ == "__main__":
    test = JSONSchema('mongo.txt')
    for document in test['1']['entities']:
        root = TreeNode()
        print( f'Schema for {document}:' )
        for List in test['1']['entities'][document]:
            for key in List:
                root.addChild(key)
        root.getFrequencies()
        print()