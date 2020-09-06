import pandas as pd
import os
import ipdb
from ...params import *

class WordObjects(object):
	def __init__(self, word, type):
		self.word = word
		self.type = type
	def __str__(self):
		return u"" + self.word + "-" + self.type

def get_words_objects(path):		
	words = pd.read_excel(os.path.join(path, r"words.xlsx"))
	word_objects = []
	
	for i, row in words.iterrows():
		word_objects.append(WordObjects(row.word, type_to_text(row.type)))

	return word_objects
	
def type_to_text(raw_type):
	return word_types[raw_type]
		

word_types = [STILL, ALIVE] # 0 is still, 1 is alive