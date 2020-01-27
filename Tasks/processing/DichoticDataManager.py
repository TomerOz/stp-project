import random
import ipdb

class DichoticTrialsManager(object):
	def __init__(self, data_manager, dichotic_name_str, n_of_chunks=None, n_of_unique_sentnces=None):
		self.data_manager = data_manager
		self.dichotic_name_str = dichotic_name_str
		
		# Task properties:
		self.n_one_back = 2
		self.n_blocks=3
		
		if n_of_chunks==None:
			self.n_of_chunks = 4
		else:
			self.n_of_chunks = n_of_chunks
		
		if n_of_unique_sentnces==None:
			self.n_of_unique_sentnces = 10
		else:
			self.n_of_unique_sentnces = n_of_unique_sentnces

		
	def __late_init__(self):
		self.neu_dichotics_sentences = self.data_manager.neu_sentences_by_phase[self.dichotic_name_str]
		self.neg_dichotics_sentences = self.data_manager.neg_sentences_by_phase[self.dichotic_name_str]
		
		self.n_of_neu_dichotics = len(self.neu_dichotics_sentences)
		self.n_of_neg_dichotics = len(self.neg_dichotics_sentences)
		
		self.blocks_dicts = []
		self.create_blocks_of_sentneces_instances()
		self.create_dichotic_trials()
		
	def build_chunk_dic(self):
		chunk_dic={}
		for i in range(self.n_of_chunks):
			chunk_dic[i+1]={} #build 4 keys for 4 chunks
		for num_chunk in chunk_dic.keys(): #adding the values = 
			neg_number_lst = random.sample(range(self.n_of_neg_dichotics),self.n_of_unique_sentnces) #10 random numbers (sentences) from 1-20
			neu_number_lst = random.sample(range(self.n_of_neu_dichotics),self.n_of_unique_sentnces)
			OneBackNeg_index_lst = random.sample(range(2,self.n_of_unique_sentnces,2), self.n_one_back) #2 random index from 2 to 19. repeatition from the third sentence.   
			OneBackNeu_index_lst = random.sample(range(2,self.n_of_unique_sentnces,2), self.n_one_back) #2 random index from 2 to 19. repeatition from the third sentence.   
			#OneBack - insert duplication of 2 indexes in neg/neu sentences lists. 
			[neg_number_lst.insert(i,neg_number_lst[i]) for i in OneBackNeg_index_lst]
			[neu_number_lst.insert(i,neu_number_lst[i]) for i in OneBackNeu_index_lst]
			
			chunk_dic[num_chunk] = {'neg':neg_number_lst, 'neu':neu_number_lst}
			
		
		##  OMER --> do you make sure that all the sentence will be eventually used
		## because how I understand your code - it is possible to sample the same self.n_of_unique_sentnces out of n_of_neg_dichotics
		## in each chunk
		
		return chunk_dic
	
			
	def create_blocks_of_sentneces_instances(self):
		# trial_types = TrialType()
		for i in range(self.n_blocks):
			block_dict = self.build_chunk_dic()
			for chunk in block_dict:
				for i, pointer in enumerate(block_dict[chunk]['neg']):
					block_dict[chunk]['neg'][i] = self.neg_dichotics_sentences[pointer]
					
				for i, pointer in enumerate(block_dict[chunk]['neu']):
					block_dict[chunk]['neu'][i] = self.neu_dichotics_sentences[pointer]
			
			self.blocks_dicts.append(block_dict)
		
	def create_dichotic_trials(self):
		for block in self.blocks_dicts:
			for chunk in block:
				for valence in block[chunk]:
					accumelated_timing = 0 # seprate accumlatation of timing for negs and neus
					for i, sentence in enumerate(block[chunk][valence]):
						block[chunk][valence][i] = DichoticTrial(sentence, accumelated_timing)
						accumelated_timing += sentence.sentence_length + 300 # adding 300 miliseconds
					

class DichoticTrial(object):
	def __init__(self, sentence, accumelated_timing):
		self.sentence = sentence
		self.accumelated_timing = accumelated_timing

    