import random
import ipdb
import pandas as pd
from ..params import *

class DichoticTrialsManager(object):
	def __init__(
					self, gui, flow, data_manager, menu, dichotic_name_str,
					n_of_chunks=None, n_of_unique_sentnces=None,
					n_trials_practice_one=N_TRIALS_PRACTICE_ONE, 
					n_trials_practice_two=N_TRIALS_PRACTICE_TWO,
					n_blocks=None,
					sessions_names=None,
					):
		
		self.data_manager = data_manager
		self.flow = flow
		self.gui = gui
		self.dichotic_name_str = dichotic_name_str
		self.menu = menu
		self.sessions_names = sessions_names

		# Task properties:
		self.n_one_back = DEFAULT_NUMBER_OF_N_BACK
		if n_blocks == None:
			self.n_blocks = DEFAULT_NUMBER_OF_BLOCKS
		else:
			self.n_blocks = n_blocks
		
		if n_of_chunks==None:
			self.n_of_chunks = DEFAULT_NUMBER_OF_CHUNCKS
		else:
			self.n_of_chunks = n_of_chunks
		
		if n_of_unique_sentnces==None:
			self.n_of_unique_sentnces = DEFAULT_NUMBER_OF_UNIQUE_SENTENCES # represents n of trials per chunk for neutral and negatives seprately
		else:
			self.n_of_unique_sentnces = n_of_unique_sentnces
			
		self.n_trials_practice_one = n_trials_practice_one
		self.n_trials_practice_two = n_trials_practice_two
		
		
	def __late_init__(self):
		if self.sessions_names == None:
			session_name = self.dichotic_name_str
		else:
			session_name = self.sessions_names[self.menu.menu_data["session"]-1] # expecting "session" field in menu to be 0 or 1

		self.neu_dichotics_sentences = self.data_manager.neu_sentences_by_phase[session_name]
		self.neg_dichotics_sentences = self.data_manager.neg_sentences_by_phase[session_name]
		
		# some more shuffeling
		random.shuffle(self.neu_dichotics_sentences)
		random.shuffle(self.neg_dichotics_sentences)
		
		self.n_of_neu_dichotics = len(self.neu_dichotics_sentences)
		self.n_of_neg_dichotics = len(self.neg_dichotics_sentences)
		
		self.blocks_dicts = []
		self.create_blocks_of_sentneces_instances()
		self.prepare_sentences_for_practice()
		self.debug_trials()
		self.gui.after(100, self.flow.next)
		
	def debug_trials(self):
		if self.sessions_names == None:
			session_name = self.dichotic_name_str
		else:
			session_name = self.sessions_names[self.menu.menu_data["session"] - 1]  # expecting "session" field in menu to be 0 or 1

		debug_data = {"neu": [], "neg": [], "chunck": [], "block": []}

		for block_counter, block in enumerate(self.blocks_dicts):
			for chunck_num in block:
				for valence in block[chunck_num]:
					for sent in block[chunck_num][valence]:
						debug_data[valence].append(sent)
				debug_data["block"] = debug_data["block"] + [block_counter]*12
				debug_data["chunck"] = debug_data["chunck"] + [chunck_num]*12
		df = pd.DataFrame(debug_data)
		df.to_excel("Debug Output/debug_trials_dichotic_session_{}.xlsx".format(session_name), index=False)

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

    