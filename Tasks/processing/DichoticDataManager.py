import random
import ipdb

from ..params import *

# To Params:
# DEFAULT_NUMBER_OF_BLOCKS = 3
# DEFAULT_NUMBER_OF_CHUNCKS = 2 # SHOULD BE 4
# DEFAULT_NUMBER_OF_UNIQUE_SENTENCES = 6 # SHOULD BE 10
# DEFAULT_NUMBER_OF_N_BACK = 2
# N_TRIALS_PRACTICE_ONE = 7
# N_TRIALS_PRACTICE_TWO = 6

class DichoticTrialsManager(object):
	def __init__(
					self, gui, flow, data_manager, dichotic_name_str, 
					n_of_chunks=None, n_of_unique_sentnces=None,
					n_trials_practice_one=N_TRIALS_PRACTICE_ONE, n_trials_practice_two=N_TRIALS_PRACTICE_TWO,
					):
		
		self.data_manager = data_manager
		self.flow = flow
		self.gui = gui
		self.dichotic_name_str = dichotic_name_str
		
		# Task properties:
		self.n_one_back = DEFAULT_NUMBER_OF_N_BACK
		self.n_blocks = DEFAULT_NUMBER_OF_BLOCKS
		
		if n_of_chunks==None:
			self.n_of_chunks = DEFAULT_NUMBER_OF_CHUNCKS
		else:
			self.n_of_chunks = n_of_chunks
		
		if n_of_unique_sentnces==None:
			self.n_of_unique_sentnces = DEFAULT_NUMBER_OF_UNIQUE_SENTENCES
		else:
			self.n_of_unique_sentnces = n_of_unique_sentnces
			
		self.n_trials_practice_one = n_trials_practice_one
		self.n_trials_practice_two = n_trials_practice_two
		
		
	def __late_init__(self):
		self.neu_dichotics_sentences = self.data_manager.neu_sentences_by_phase[self.dichotic_name_str]
		self.neg_dichotics_sentences = self.data_manager.neg_sentences_by_phase[self.dichotic_name_str]
		
		# some more shuffeling
		random.shuffle(self.neu_dichotics_sentences)
		random.shuffle(self.neg_dichotics_sentences)
		
		self.n_of_neu_dichotics = len(self.neu_dichotics_sentences)
		self.n_of_neg_dichotics = len(self.neg_dichotics_sentences)
		
		self.blocks_dicts = []
		self.create_blocks_of_sentneces_instances()
		self.prepare_sentences_for_practice()
		self.gui.after(100, self.flow.next)
		
	def prepare_sentences_for_practice(self):
		practice_one_sents = random.sample(self.neu_dichotics_sentences, self.n_trials_practice_one)
		p1_left_sentences = random.sample(practice_one_sents, int(round(len(practice_one_sents)/2)))
		p1_right_sentences = [sent for sent in practice_one_sents if sent not in p1_left_sentences]
		
		
		practice_two_sents = random.sample(self.neu_dichotics_sentences, self.n_trials_practice_two)
		p2_left_sentences = random.sample(practice_two_sents, int(round(len(practice_two_sents)/2)))
		p2_right_sentences = [sent for sent in practice_two_sents if sent not in p2_left_sentences]
		
		# duplicate one sentence and save lists:
		self.p1_left_sentences = self.duplicate_one_sentence(p1_left_sentences)
		self.p1_right_sentences = self.duplicate_one_sentence(p1_right_sentences)
		self.p2_left_sentences = self.duplicate_one_sentence(p2_left_sentences)
		self.p2_right_sentences = self.duplicate_one_sentence(p2_right_sentences)
		
	def duplicate_one_sentence(self, sentences):
		random_pointer = random.randint(1, len(sentences)-1)
		sentences.insert(random_pointer, sentences[random_pointer])
		return sentences
		
	def build_chunk_dic(self):
		chunk_dic={}
		for i in list(range(self.n_of_chunks)):
			chunk_dic[i+1]={} #build 4 keys for 4 chunks
		for num_chunk in chunk_dic.keys(): #adding the values = 
			neg_number_lst = random.sample(list(range(self.n_of_neg_dichotics)),self.n_of_unique_sentnces) #10 random numbers (sentences) from 1-20
			neu_number_lst = random.sample(list(range(self.n_of_neu_dichotics)),self.n_of_unique_sentnces)
			OneBackNeg_index_lst = random.sample(list(range(2,self.n_of_unique_sentnces,2)), self.n_one_back) #2 random index from 2 to 19. repeatition from the third sentence.   
			OneBackNeu_index_lst = random.sample(list(range(2,self.n_of_unique_sentnces,2)), self.n_one_back) #2 random index from 2 to 19. repeatition from the third sentence.   
			#OneBack - insert duplication of 2 indexes in neg/neu sentences lists. 
			[neg_number_lst.insert(i,neg_number_lst[i]) for i in OneBackNeg_index_lst]
			[neu_number_lst.insert(i,neu_number_lst[i]) for i in OneBackNeu_index_lst]
			
			chunk_dic[num_chunk] = {'neg':neg_number_lst, 'neu':neu_number_lst}
			
		return chunk_dic
	
	def create_blocks_of_sentneces_instances(self):
		# trial_types = TrialType()
		for i in list(range(self.n_blocks)):
			block_dict = self.build_chunk_dic()
			for chunk in block_dict:
				for i, pointer in enumerate(block_dict[chunk]['neg']):
					block_dict[chunk]['neg'][i] = self.neg_dichotics_sentences[pointer]
					
				for i, pointer in enumerate(block_dict[chunk]['neu']):
					block_dict[chunk]['neu'][i] = self.neu_dichotics_sentences[pointer]
			
			self.blocks_dicts.append(block_dict)
			
	def create_list_of_chanks_ears_volumes(self): #[0,0,1,1] - for 4 chanks, each is 0 or 1 is for left_neg
			list_of_chanks_ears = [0]*(int(self.n_of_chunks/2)) + [1]*(int(self.n_of_chunks/2))
			random.shuffle(list_of_chanks_ears)
			self.list_of_chanks_ears_volumes = list_of_chanks_ears


class DichoticTrial(object):
	def __init__(self, sentence, accumelated_timing):
		self.sentence = sentence
		self.accumelated_timing = accumelated_timing

    