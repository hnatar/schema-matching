#!/usr/bin/env python3

"""
Markov text generator, to create 'random' samples.
"""
import markovify

# Get raw text as string.
with open("firstnames.txt") as f:
    text = f.read()
print(text)

# Build the model.
text_model = markovify.NewlineText(text)

# Print five randomly-generated sentences
for i in range(5):
    print(text_model.make_sentence(tries=10000))

# Print three randomly-generated sentences of no more than 140 characters
for i in range(3):
    print(text_model.make_short_sentence(140))
