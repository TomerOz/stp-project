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
NUM_OF_INTIAL_NEUTRAL_REAL_TRIALS = 4


class MainAudioProcessor(object):
	
	def __init__(self):
		pass		
		
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
		self.pre_intervention_sentences = []
		self.post_intervention_sentences = []
		
		self.process_sentences_data() # sentence are read from excel and located at dir an classified by valence *HERE PRE LOAD SHOULD HAPPEN*
		self._split_train_and_post_trials()
		self._randomize_sentences()	# randomization with 4 starter neutrals
		
		
		
	def _split_train_and_post_trials(self):
		len_neutrals = len(self.neutral_sentences)
		len_negatives = len(self.negatives_sentences)
		
		half_nutrals = int(len_neutrals/2.0)
		half_negatives = int(len_negatives/2.0)
		
		self.training_neutrals = self.neutral_sentences[0:half_nutrals]
		self.post_training_neutrals = self.neutral_sentences[half_nutrals:len_neutrals]
		self.training_negatives = self.negatives_sentences[0:half_negatives]
		self.post_training_negatives = self.negatives_sentences[half_negatives:len_negatives]
		
		self.pre_intervention_sentences = self.training_neutrals + self.training_negatives
		random.shuffle(self.pre_intervention_sentences)
		self.post_intervention_sentences = self.post_training_neutrals + self.post_training_negatives
		random.shuffle(self.post_intervention_sentences)
		

	def _randomize_sentences(self):
		''' only for initial randomization - additional shufflinfs will be required whithin each phase/task.
		randomizes sentences pointers - ensures:
		- first four are neutral 
		- last four are neutral ?
		'''
		# taking 4 sentences fot the begining 
		start_trials = random.sample(self.neutral_sentences, NUM_OF_INTIAL_NEUTRAL_REAL_TRIALS)
		for s in start_trials:
			self.sentences.remove(s) #removes 4 start neutrals from all sentences
		
		random.shuffle(self.sentences) # shuffeling without 4 starts
		self.sentences =  start_trials + self.sentences # updating sentences

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