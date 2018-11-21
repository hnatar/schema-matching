#!/usr/bin/env python3

import collections
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

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
    def __init__(self, label):
        self.label = label
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
        r = 0.0
        for i in range(0, len(word)):
            if (i not in self.freq) or (word[i] not in self.freq[i]):
                r += np.log( self.CharCount[word[i]]+1 ) - np.log( self.CharTotal+1 )
            else:
                r += np.log(self.freq[i][word[i]]) - np.log( sum(self.freq[i].values()) )
        return r
    def stats(self):
        print( f'Statistics for {self.label}:' )
        print( 'Mean Length: ', '%.2f' % np.mean(self.observed_len) )
        print( 'Variance Length: ', '%.2f' % np.var(self.observed_len) )

class SequenceModel:
    def __init__(self, ListOfModels):
        self.seq = ListOfModels
        self.len = [ random.randint(1, 10) for i in self.seq ]

    def logprob(self, word):
        r = 0.0
        cur = 0
        for model in range(0, len(self.seq)):
            curword, word = word[:self.len[model]], word[self.len[model]:]
            if not curword:
                return r
            r += self.seq[model].logprob(word)
        return r


if __name__ == "__main__":
    Names = CharDistribution('Names')
    Phone = CharDistribution('Phone')
    NameList = []
    PhoneList = []

    with open('firstnames.txt', 'r') as f:
        for name in f.readlines():
            name = name.strip()
            Names.seen_word(name)
            NameList.append(name)
    Names.stats()

    with open('phonenum.txt', 'r') as f:
        for phone in f.readlines():
            phone = phone.strip()
            Phone.seen_word(phone)
            PhoneList.append(phone)
    Phone.stats()

    table = []
    for i in range(10):
        r1 = random.choice(range(len(NameList)))
        r2 = random.choice(range(len(PhoneList)))
        # 1 or 2 are ground truth labels (name or phone, to make reading easier)
        table.append( (1, '%15s %.2f %.2f' % (NameList[r1], Names.logprob(NameList[r1]), Phone.logprob(NameList[r1]))) )
        table.append( (2, '%15s %.2f %.2f' % (PhoneList[r2], Names.logprob(PhoneList[r2]), Phone.logprob(PhoneList[r2]))) )
    table = sorted(table)
    for i, row in enumerate(table):
        print( '%3d %s' % (i, row[1]) )

