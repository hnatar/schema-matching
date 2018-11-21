#!/usr/bin/env python3

import nltk
import string

source = 'userstory.txt'
out = 'userwords.txt'
english_stopwords = set(nltk.corpus.stopwords.words('english'))
already_added = set()

with open(out, 'w') as f2:
    with open(source, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            line = line.lower()
            for word in nltk.word_tokenize(line):
                word = ''.join(filter(lambda x: x not in string.punctuation, word))
                print('word=', word)
                if word in english_stopwords:
                    continue
                if word in already_added:
                    continue
                if not word:
                    continue
                f2.write(f'{word}\n')
                already_added.add(word)

