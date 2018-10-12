#!/usr/bin/env python3

import collections
import matplotlib
import matplotlib.pyplot as plt

class CharDistribution:
    def __init__(self):
        self.freq = collections.defaultdict(dict)
    def seen(self, pos, char):
        if pos not in self.freq:
            self.freq[pos] = collections.defaultdict(int)
        self.freq[pos][char] += 1
    def plot(self, pos):
        print( self.freq[pos].keys() )
        print( self.freq[pos].values() )
        plt.bar( list(self.freq[pos].keys()), list(self.freq[pos].values()) )
        plt.show()
    def prob(self, word):
        r = 1.0
        decay = 0.6
        for i in range(0, len(word)):
            if (i not in self.freq) or (word[i] not in self.freq[i]):
                if r == 0 or i == 0:
                    return 0
                else:
                    r *= decay
            else:
                r *= self.freq[i][word[i]]
        return r


tmp = CharDistribution()
with open('names.txt', 'r') as f:
    for name in f.readlines():
        name = name.strip()
        for i in range(0, len(name)):
            tmp.seen(i, name[i])
print( tmp.prob('123') )


