#!/usr/bin/env python3

import sys

import collections
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

import fetch_data

"""
Given sample training data for all classes, use Naive-Bayes at character level
to find the most likely class. Positional characters form the features.

P(word | class1) = P(class1) * P(char 1 | class1) * P(char2 | class1) * P(char3 | class1) ...
Maximizing this is same as maximizing log P(word | class1)
which is
    log P(class1) + log P(char1|class1) + log P(char2|class1) + log P(char3|class1) ...

Log prob. to minimize underflow issue, compare P(word|class1) and P(word|class2) etc and get max / most likely class
"""

class CharDistribution:
    def __init__(self):
        self.freq = collections.defaultdict(dict)
        self.CharCount = collections.defaultdict(int)
        self.CharTotal = 0
        self.observed_len = []
    def seen(self, pos, char):
        if pos not in self.freq:
            self.freq[pos] = collections.defaultdict(int)
        self.freq[pos][char] += 1
        self.CharCount[char] += 1
        self.CharTotal += 1
    def seen_word(self, word):
        self.observed_len.append( len(word) )
        for i in range(0, len(word)):
            self.seen(i, word[i])
    def plot(self, pos):
        print( self.freq[pos].keys() )
        print( self.freq[pos].values() )
        plt.bar( list(self.freq[pos].keys()), list(self.freq[pos].values()) )
        plt.show()
    def logprob(self, word):
        r = scipy.stats.norm( *self.stats() ).pdf( len(word) )
        for i in range(0, len(word)):
            if (i not in self.freq) or (word[i] not in self.freq[i]):
                r += np.log( self.CharCount[word[i]]+1 ) - np.log( 1 + self.CharTotal+ len(self.freq[i].keys()) )
            else:
                r += np.log(self.freq[i][word[i]]) - np.log( sum(self.freq[i].values()) )
        return r
    def stats(self):
        if not self.observed_len:
            return (0.0, 1.0)
        return ( np.mean(self.observed_len), np.std(self.observed_len)+0.0001, )

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('usage: python3 [Model] <space separated list of fields to compare against>')
        sys.exit()
    field, compare_with = sys.argv[1], sys.argv[2:]
    assert len(field) > 0, 'Fieldname cannot be empty'

    print('Field=', field)

    def get_model_src(name):
        assert len(name) > 0, 'Model name cannot be empty'
        # where the data is being fetched from.
        # Can be a field inside MongoDB, or can be a newline 
        # delimited .txt file. If .txt file, checks in predefined path
        File = 'FieldData/' + name + '.txt'
        if name[0] == '/':
            # used to signify data is from Mongo
            _,db,col,_field = name.split('/')
            fetch_data.write_to_file(db, col, _field)
            File = 'FieldData/MONGO_' + '_'.join([db,col,_field]) + '.txt'
        Model = CharDistribution()
        with open(File, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                Model.seen_word(line)
        return Model

    m1 = get_model_src( field )
    Similarity = {}
    for m in compare_with:
        File = 'FieldData/' + m + '.txt'
        if m[0] == '/':
            _, db, col, _field = m.split('/')
            fetch_data.write_to_file(db,col,_field)
            File = 'FieldData/MONGO_' + '_'.join([db,col,_field]) + '.txt'
        mean_sim = 0.0
        tok = 0.0
        worst = None
        best= None
        with open(File, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line == 'undefined':
                    continue
                p = m1.logprob(line)
                print(line, 'prob=', p)
                mean_sim += p
                if worst == None:
                    worst = p
                else:
                    worst = min(worst, p)
                if best == None:
                    best = p
                else:
                    best = max(best, p)
                tok += 1.0
        Similarity[m] = (mean_sim / tok, worst, best)
    title= 'Similarity with field=' + field
    print(title)
    print('-'*len(title))
    List = []
    for k in Similarity:
        print(field, k, Similarity[k][1])
        List.append( (Similarity[k][1], k,) )
    List = sorted(List, reverse=True)
    print('-'*5)
    print('Top 3 similar items: ')
    for item in List[:3]:
        print(item[1])
    sys.exit()
