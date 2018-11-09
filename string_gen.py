#!/usr/bin/env python3

"""
String generators

Generate strings which adhere to a specific pattern,
e.g. lowercase, Firstname Lastname, or CamelCased, or A.B.C,
hyphenated, etc.This is mainly used to train the ML models.

Because Python 3 strings are UTF-8, this should handle
languages like Chinese as well.
"""

import numpy as np

class StringGenerator:
	def __init__(self, max_string_length=10):
		self.max_string_length = max_string_length

	def generate(self):
		while True:
			block_size = np.random.random_integers(1, self.max_string_length)
			s = ''
			for i in range(0, block_size):
				rand_char = np.random.random_integers(0, 25)
				s += chr( ord('A') + rand_char )
			yield s

def lowercase(string_generator):
	default_init = string_generator.__init__
	default_generate = string_generator.generate
	class LowercaseGenerator:
		def __init__(self, *args, **kwargs):
			default_init(self, *args, **kwargs)
		
		def generate(self):
			for x in string_generator.generate(self):
				yield x.lower()
	return LowercaseGenerator

def camel_case(string_generator):
	default_init = string_generator.__init__
	default_generate = string_generator.generate
	class CamelCaseGenerator:
		def __init__(self, *args, **kwargs):
			default_init(self, *args, **kwargs)
		
		def generate(self):
			for x in string_generator.generate(self):
				r = ''
				for i, c in enumerate(x):
					if i == 0 or x[i-1] == ' ':
						r += c.upper()
					else:
						r += c.lower()
				yield r
	return CamelCaseGenerator


def whitespace_noise(string_generator):
	default_init = string_generator.__init__
	default_generate = string_generator.generate
	class WhitespaceNoiseGenerator:
		def __init__(self, *args, **kwargs):
			default_init(self, *args, **kwargs)
		
		def generate(self):
			for x in string_generator.generate(self):
				rand_places = np.random.random_integers(0, 1)
				res = x.lower()
				rand_indices = np.random.random_integers(0, len(res), rand_places)
				for x in rand_indices:
					res = res[:x] + ' ' + res[x:]
				yield res
	return WhitespaceNoiseGenerator

@camel_case
@lowercase
@whitespace_noise
class custom_gen(StringGenerator):
	pass
