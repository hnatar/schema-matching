# Readme

This branch contains the name level matching code.

## Approach

Since matching can be done for one collection across semesters, or
across multiple collections, input taken as two lists of field names.

Many of the fields may be common/same, these are matched together first.
Unmatched names are then chunked, and matched to get overall max similarity.

Chunks are based on entities from user stories, which are stored in a pickled trie.
To regenerate this dictionary, please run `python3 trie.py`. Prefix matching is done,
currently a minimum length >= 3 is needed to match.
