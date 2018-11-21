#!/usr/bin/env python3

"""
Simple trie implementation
"""

import pickle

class Trie:
    def __init__(self, letter = '', parent = None):
        self.letter = letter
        self.parent = parent
        self.children = {}
        self.word = (self.parent.word+letter) if self.parent else ""
        self.is_word = False

    def insert(self, word):
        cur = self
        for c in word:
            c = c.lower()
            if not (c in cur.children):
                cur.children[c] = Trie(letter=c, parent=cur)
            cur = cur.children[c]
        cur.is_word = True

    def find(self, word, prefix_match=0):
        cur = self
        for c in word:
            #print('cur=', cur)
            if not cur:
                return False
            c = c.lower()
            if (c in cur.children):
                cur = cur.children[c]
            else:
                return False
        return True if prefix_match else cur.is_word

    def get_prefix(self):
        matched = []
        dfs = [ self ]
        while dfs:
            node = dfs.pop()
            #print('at node', node, 'word=', node.word)
            if len(node.word) >= 3:
                matched.append(node.word)
            for c in node.children:
                #print('appending for ', c)
                dfs.append(node.children[c])
        return matched

if __name__ == "__main__":
    # TODO: add tests
    root = Trie()
    print('Reading names')
    with open('userwords.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            root.insert(line)
    with open('pickled_userwords', 'wb') as out:
        pickle.dump(root, out)
    with open('pickled_userwords', 'rb') as inp:
        rt2 = pickle.load(inp)
    print( rt2.get_prefix() )

