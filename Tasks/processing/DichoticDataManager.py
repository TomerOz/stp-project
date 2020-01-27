import random
from TasksAudioDataManager import TrialType

self.n_of_neg_dichotics=20
self.n_of_neu_dichotics=20

NumBlock=3 
NumChunk = 4 #per block 
NumUnique = 10 #per chunk
NumOneBack = 2 #per chunk

class DichoticTrials(object):
	def __init__(self, data_manager, dichotic_name_str):
		self.data_manager = data_manager
		self.dichotic_name_str = dichotic_name_str
		
		self.neg_dichotics = self.data_manager.neg_sentences_by_phase[dichotic_name_str]
		self.neu_dichotics = self.data_manager.neu_sentences_by_phase[dichotic_name_str]
		
		self.n_of_neg_dichotics = len(self.data_manager.neg_sentences_by_phase[dichotic_name_str])
		self.n_of_neu_dichotics = len(self.data_manager.neu_sentences_by_phase[dichotic_name_str])
		
		
	def build_chunk_dic(self, NumChunk, NumUnique, NumOneBack):
		chunk_dic={}
		for i in range(NumChunk):
			chunk_dic['Chunk'+str(i+1)]={} #build 4 keys for 4 chunks
		for num_chunk in chunk_dic.keys(): #adding the values = 
			neg_number_lst = random.sample(range(1,self.n_of_neg_dichotics+1),NumUnique) #10 random numbers (sentences) from 1-20
			neu_number_lst = random.sample(range(1,self.n_of_neu_dichotics+1),NumUnique,)
			OneBackNeg_index_lst = random.sample(range(2,NumUnique,2), NumOneBack) #2 random index from 2 to 19. repeatition from the third sentence.   
			OneBackNeu_index_lst = random.sample(range(2,NumUnique,2), NumOneBack) #2 random index from 2 to 19. repeatition from the third sentence.   
			#OneBack - insert duplication of 2 indexes in neg/neu sentences lists. 
			[neg_number_lst.insert(i,neg_number_lst[i]) for i in OneBackNeg_index_lst]
			[neu_number_lst.insert(i,neu_number_lst[i]) for i in OneBackNeu_index_lst]
	
			chunk_dic[num_chunk] = {'neg':neg_number_lst, 'neu':neu_number_lst}
		return chunk_dic
		
	def build_blocK_dic(self, NumBlock):
	#continure here after talking with Iftach about the sequence within block 
		block_dic={}
		for i in range(NumBlock):
			# Left_list = random.sample(#[1,0,0,1]
			cunk_dic = build_chunk_dic(self.n_of_neg_dichotics,self.n_of_neu_dichotics,NumChunk,NumUnique,NumOneBack)
			pass
			
	def create_trial_types(self):
		# trial_types = TrialType()
            

        
    