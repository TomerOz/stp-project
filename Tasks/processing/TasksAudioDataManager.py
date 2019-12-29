import pandas as pd
import os
import random

PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
AUDIO_FILES_DIRECTORY = 'audio_files_wav'


# sentences excel column names
LENGTH_COL = 'length'
SENTENCE_TEXT = 'sentContent'
SENTENCE_VALENCE = 'SentenceType'
SENTENCE_NUM = 'TAPlistNumber'
SENTENCE = 'sentence'

ONE_MILISCOND = 1000
MILISECONDS_BEFORE_END = 500

# task properties
NEGATIVE_SENTENCE = 'neg' 			# According to audio df excel file
NEUTRAL_SENTENCE = 'ntr'			# According to audio df excel file

class MainAudioProcessor(object):
	
	def __init__(self, phases_names=None, n_trials_by_phase=None, n_practice_trials=None):
		
		self.phases_names = phases_names # A list of strings representing phases names
		self.n_phases = len(self.phases_names) # Ammount of experimentatl phases to split sentence to
		self.n_trials_by_phase = n_trials_by_phase # ammount of trials per phase - a dictionary -  determines how many sentence repetition should occur
		
		if n_practice_trials == None:
			self.n_practice_trials=8
		else:
			self.n_practice_trials = n_practice_trials
			
		self.n_min_practice_trials = 3
		self.ammount_practice_trials = None # To be determined according to sentences ammopunt relaity 3 or 8
		self.n_start_neutral_trials = 4 # real data trials
	def __late_init__(self, menu):	
		self.menu = menu
		# audio paths and df
		self.audio_path = self.menu.updated_audio_path # path of dir containing audio dir of audio and audio df 
		self.audio_df = pd.read_excel(self.audio_path + '\\' + PROCESSED_AUDIO_DF) # path of audio data excel file
		self.audio_files_path = self.audio_path + '\\' + AUDIO_FILES_DIRECTORY  # path of dir containing recording files
		self.sentence_inittial_path = self.audio_files_path + '\\' # the initial path of every recording
		self.audio_files_list = os.listdir(self.audio_files_path) # list of recording names
		
		# sentences info
		self.sentences = [] # sentences to be used in the current phase - be it pre or post trainig -- updates within program
		self.neutral_sentences = [] # contain all neutral sentences
		self.negatives_sentences = [] # contain all negative sentences
		
		self.neu_sentences_by_phase = {} # A dictionary that holds unique neutral sentences of each phase, number of phases is predetermined by console.py user.
		self.neg_sentences_by_phase = {} # the same but negative
		self.sentences_by_phase = {} # sentences by phase after shuffeling, and multplying ammount of sentences accordind to desired ammount of trials by phase
		
		self.process_sentences_data() # sentence are read from excel and located at dir an classified by valence *HERE PRE LOAD SHOULD HAPPEN*
		self._split_senteces_to_phases()
		
	def _split_senteces_to_phases(self):
		
		'''
		This functions splits the neutral and negative sentences into a requested ammount of phases
				
		'''
		local_neurtrals = [] + self.neutral_sentences
		local_negatives = [] + self.negatives_sentences
		
		n_per_phase_neutrals = int(1.0*len(self.neutral_sentences) / self.n_phases)
		n_per_phase_negs = int(1.0*len(self.negatives_sentences) / self.n_phases)
		
		for phase in self.phases_names:
			sample_neus =  random.sample(local_neurtrals, n_per_phase_neutrals)
			sample_negs = random.sample(local_negatives, n_per_phase_negs)
			
			self.neu_sentences_by_phase[phase] = sample_neus # +
			self.neg_sentences_by_phase[phase] = sample_negs # -
			
			# Unifing the neutrals and negatives
			self.sentences_by_phase[phase] = sample_neus + sample_negs
			
			# multiplying to fit desired amount of trials in phase
			rounded_multplying_factor = round(1.0*self.n_trials_by_phase[phase]/len(self.sentences_by_phase[phase]))
			self.sentences_by_phase[phase] = self.sentences_by_phase[phase] * int(rounded_multplying_factor)
			
			# taking 4 of neutral trials and saving them aside, later be added at the begining right after practice
			sample_of_initial_4_neutrals = random.sample(sample_neus, self.n_start_neutral_trials) # for the running mean
			self.sentences_by_phase[phase] = [e for e in self.sentences_by_phase[phase] if e not in sample_of_initial_4_neutrals] # taking intial 4 from the neutral sentence, later be added
			self.sentences_by_phase[phase] = self.sentences_by_phase[phase] + sample_of_initial_4_neutrals # becase the former delets these four as many times as the multiplyin factor ddetermines
			
			# randimization - CURRENTLY STUPID
			random.shuffle(self.sentences_by_phase[phase])
			
			# Adding practice trials --> cuurently multplying existing neutrasl
			if len(sample_neus) >= self.n_practice_trials:
				practice_trials = random.sample(sample_neus, self.n_practice_trials) # 8 is the default number of practice trials
			else:
				try:
					practice_trials = random.sample(sample_neus, self.n_min_practice_trials) # 8 is the default number of practice trials
				except: 
					raise Exception("Too little neutrals sentences to sample practice trials")
			
			for sent in practice_trials:
						sent.is_practice = True
			self.sentences_by_phase[phase] = [] + practice_trials + sample_of_initial_4_neutrals + self.sentences_by_phase[phase]
			
			# updating ammount of practice trials
			self.ammount_practice_trials = len(practice_trials)
			
			# Updating the local sentences lists - removing those that were samples
			local_neurtrals = [e for e in local_neurtrals if e not in sample_neus]
			local_negatives = [e for e in local_negatives if e not in sample_negs]
			
		

	def _get_sentence_num(self, file_name):
		split_1 = file_name.split(SENTENCE)
		split_2 = split_1[1].split('_')
		sentence_num = int(split_2[0])
		return sentence_num
		
		
	def process_sentences_data(self):
		sentences_nums = []
		for sentence in self.audio_files_list:
			sentences_nums.append(self._get_sentence_num(sentence))
		
		for i in range(len(self.audio_df)):
			text = self.audio_df.loc[i, SENTENCE_TEXT]
			valence = self.audio_df.loc[i, SENTENCE_VALENCE]
			num_in_excel = self.audio_df.loc[i, SENTENCE_NUM]
			sentence_length = self.audio_df.loc[i, LENGTH_COL]
			index_of_path = sentences_nums.index(num_in_excel) #gets index of file path based on sentence num in the audio excel
			extracted_num = sentences_nums[index_of_path] # num based on file name -- for validation
			sentence_path = self.audio_files_list[index_of_path]
			
			self.sentences.append(Sentence(text, valence, extracted_num, num_in_excel, sentence_path, sentence_length))
		
		# classifing sentences by valence
		for s in self.sentences:
			if s.valence == NEGATIVE_SENTENCE:
				self.negatives_sentences.append(s)
			elif s.valence == NEUTRAL_SENTENCE:
				self.neutral_sentences.append(s)
		# shuffeling neutral and negative trials
		random.shuffle(self.neutral_sentences)
		random.shuffle(self.negatives_sentences)
			
class Sentence(object):
	
	def __init__(self, text, valence, num, num_in_excel, file_path, sentence_length):
		self.text = unicode(text)
		self.valence = valence
		self.num = num
		self.num_in_excel = num_in_excel
		self.file_path = file_path
		self.sentence_length = sentence_length*ONE_MILISCOND # in miliseconds
		self.digit_que = int(self.sentence_length-MILISECONDS_BEFORE_END) # time of sentence start
		self.is_practice = False