#!/usr/bin/env python3

"""
Schema Matching

0.1.0		- Proof of concept for simple instance matching based on values ranges (for numeric),
			  predicted category / type of data (string, int, option-type, etc.).
			  Membership in category is a simple feature, features are fed to a classifier which
			  can be decision tree or logistic multiclass.

			  Value range modelling based on GAN approach ?
"""

import pdb
import string_gen

DEBUG = True

if __name__ == "__main__":
    stringen = string_gen.custom_gen()
    stringen = stringen.generate()
    for i in range(0, 1000):
        print( next(stringen) )
    return 0

