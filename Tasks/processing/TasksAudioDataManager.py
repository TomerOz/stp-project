import pandas as pd
import os
import random
import ipdb
import copy
import numpy as np

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

AFACT_PHASE = "afact_phase"			# in console we must use these contants
DICHOTIC_PHASE = "dichotic_phase"

class MainAudioProcessor(object):
	
	def __init__(self, 
						phases_names=None, 
						n_start_neutral_trials =None, 
						n_trials_by_phase=None, 
						n_practice_trials=None, 
						phases_distribution_percent_dict=None, 
						precent_of_catch_trials=None, 
						phases_without_catch_trials=None,
						n_block_per_phase=None,
						):
		
		self.phases_names = phases_names # A list of strings representing phases names
		self.n_phases = len(self.phases_names) # Ammount of experimentatl phases to split sentence to
		self.n_trials_by_phase = n_trials_by_phase # ammount of trials per phase - a dictionary -  determines how many sentence repetition should occur
		self.afact_phase = AFACT_PHASE
		
		if n_practice_trials == None:
			self.n_practice_trials=8
		else:
			self.n_practice_trials = n_practice_trials
		
		if precent_of_catch_trials==None:
			self.precent_of_catch_trials = 3.0/8.0
		else:
			self.precent_of_catch_trials = precent_of_catch_trials
		
		if n_start_neutral_trials==None:
			self.n_start_neutral_trials = 4 # real data trials
		else:
			self.n_start_neutral_trials = n_start_neutral_trials
		
		if phases_without_catch_trials==None:
			self.phases_without_catch_trials = [] # means that all phases needs catch trials
		else:
			self.phases_without_catch_trials = phases_without_catch_trials
			
		if n_block_per_phase==None:
			self.n_block_per_phase = {} # means that all phases have two blocks
			for phase in self.phases_names:
				self.n_block_per_phase[phase] = 2
		else:
			self.n_block_per_phase = n_block_per_phase 
			for phase in self.phases_names:
				if not phase in self.n_block_per_phase:
					self.n_block_per_phase[phase] = 2 # means that all phases that where not specified, are of two phases
		
		self.phases_distribution_percent_dict = phases_distribution_percent_dict
		
		self.trial_sentence_refetnce = None # later being created as a class instance of TrialsSentencesReff
		
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
		self.catch_and_non_catch_trials_list_by_phase = {} # will be filled by create_catch_trials()
		
		self.neu_sentences_by_phase = {} # A dictionary that holds unique neutral sentences of each phase, number of phases is predetermined by console.py user.
		self.neg_sentences_by_phase = {} # the same but negative
		self.sentences_by_phase = {} # sentences by phase after shuffeling, and multplying ammount of sentences accordind to desired ammount of trials by phase
		
		self.trials_types_by_phase = {} #  per phase, list of TYPES as strings "ntr", "neg" or "prac"
		self.sentences_instances_by_type_by_phase = {} # per phase, with index and type, SENTNECE INSTANCE
		self.sentence_trial_reffs_by_phase = {} # contains TrialsSentencesReff instances by phase
		self.change_block_trials_by_phase = {} # each phase change block trial refference

		self.process_sentences_data() # sentence are read from excel and located at dir an classified by valence *HERE PRE LOAD SHOULD HAPPEN*
		self._split_senteces_to_phases()
		self.create_catch_trials()
		self.fill_sentence_trial_refferences()
		self.insert_catch_trials_trial_types()
		self.insert_feedback_trialtypes_on_afact_phase()
		self.define_change_block_trials_per_phase()
		ipdb.set_trace()
	def _split_senteces_to_phases(self):
		'''
		This functions splits the neutral and negative sentences into a requested ammount of phases
		 IF U WAN'T THE DIFFERENT PHASES TO NOT HAVE EQUAL AMMOUNT OF UNIQUE SENTENCES JUST SAY SO AND ACT IN THIS PLACE +_+_+_+_+_+_+_+_+_+	
		'''
		local_neurtrals = [] + self.neutral_sentences
		local_negatives = [] + self.negatives_sentences
		
		n_per_phase_neutrals = 	int(round(1.0*len(self.neutral_sentences) / self.n_phases))
		n_per_phase_negs = 		int(round(1.0*len(self.negatives_sentences) / self.n_phases))
		
		for phase in self.phases_names:
			# Choosing the unique sentences (+ and -) for each phase
			if self.phases_distribution_percent_dict==None:
				sample_neus =  random.sample(local_neurtrals, n_per_phase_neutrals)
				sample_negs = random.sample(local_negatives, n_per_phase_negs)
			else:
			# +_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_ phases_distribution_percent_dict expected to be a dictionariy of percents (floats) +_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_
				n_per_phase_neutrals = 	int(round(1.0*len(self.neutral_sentences)*self.phases_distribution_percent_dict[phase]))
				n_per_phase_negs = 		int(round(1.0*len(self.negatives_sentences)*self.phases_distribution_percent_dict[phase]))
				
				sample_neus = 	random.sample(local_neurtrals, n_per_phase_neutrals)
				sample_negs = 	random.sample(local_negatives, n_per_phase_negs)
			# +_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_
			
			self.neu_sentences_by_phase[phase] = sample_neus # +
			self.neg_sentences_by_phase[phase] = sample_negs # -
			# Suffeling
			random.shuffle(self.neu_sentences_by_phase[phase])
			random.shuffle(self.neg_sentences_by_phase[phase])
			# Unifing the neutrals and negatives
			self.sentences_by_phase[phase] = sample_neus + sample_negs
			
			self._create_trials_pointers_by_phase(phase)
			
			# Updating the local sentences lists - removing those that were sampled
			local_neurtrals = [e for e in local_neurtrals if e not in sample_neus]
			local_negatives = [e for e in local_negatives if e not in sample_negs]
		# AT this point i have unique neus and negs per phase
	def _create_trials_pointers_by_phase(self, phase):
		
		# rounded_multplying_factor by using it I know how many repetition per sentence
		ammount_unique_sentences = len(self.sentences_by_phase[phase])
		rounded_multplying_factor = int(round(1.0*self.n_trials_by_phase[phase]/ammount_unique_sentences))
		# creating intial pointers
		neus_pointers = range(len(self.neu_sentences_by_phase[phase]))
		negs_pointers = range(len(self.neg_sentences_by_phase[phase]))
		# Adding practice trials --> cuurently multplying existing neutrasl
		practice_trials_pointers = random.sample(neus_pointers, self.n_practice_trials) # 8 is the default number of practice trials
		# first shuffeling of originals:
		random.shuffle(neus_pointers)
		random.shuffle(negs_pointers)
		
		# creating additional pointers to fit desired amount of trials
		lists_of_additional_neus_pointers = []
		lists_of_additional_negs_pointers = []
		ammount_of_additions = rounded_multplying_factor-1
		for i in range(ammount_of_additions):
			additional_neus_pointers = [] + neus_pointers
			additional_negs_pointers = [] + negs_pointers
			# shuffeling:
			random.shuffle(additional_neus_pointers)
			random.shuffle(additional_neus_pointers)
			# adding to a list of lists
			lists_of_additional_neus_pointers.append(additional_neus_pointers)
			lists_of_additional_negs_pointers.append(additional_negs_pointers)
				
		# adding additional with intial
		for additional_neus in lists_of_additional_neus_pointers:
			neus_pointers = neus_pointers + additional_neus
			
		for additional_negs in lists_of_additional_negs_pointers:
			negs_pointers = negs_pointers + additional_negs
		
		
		# Checking if multiplying reached the desired ammount of trials
		if len(neus_pointers)*2 < self.n_trials_by_phase[phase]:
			delta = int(round((self.n_trials_by_phase[phase] - len(neus_pointers)*2)/2.0))
			neu_additional_pointers = random.sample(neus_pointers,delta)
			neg_additional_pointers = random.sample(negs_pointers,delta)
			neus_pointers = neus_pointers + neu_additional_pointers
			negs_pointers = negs_pointers + neg_additional_pointers

		elif len(neus_pointers)*2 > self.n_trials_by_phase[phase]:
			pointers_to_sample = int(round(self.n_trials_by_phase[phase]/2.0))
			neus_pointers = random.sample(neus_pointers,pointers_to_sample)
			negs_pointers = random.sample(negs_pointers,pointers_to_sample)
		
		# creating an all trials dictionary
		PRACTICE_SENTENCE = "prac"
		neu = TrialType(NEUTRAL_SENTENCE)
		neg = TrialType(NEGATIVE_SENTENCE)
		practice = TrialType(PRACTICE_SENTENCE)
		practice.is_practice = True
		# arranging trials:
		trials = [neu]*(len(neus_pointers)-self.n_start_neutral_trials) + [neg]*len(negs_pointers) # - n_start_neutral_trials is for the intial four neus to be later added
		random.shuffle(trials)
		
		# creating new instances with deep copy for practice trials
		practice_trials_sentences = []
		for prac_pointer in practice_trials_pointers:
			dc = copy.deepcopy(self.neu_sentences_by_phase[phase][prac_pointer])
			dc.is_practice = True
			practice_trials_sentences.append(dc)
		
		# Saving final values
		prac_neu_or_neg = {
						PRACTICE_SENTENCE: practice_trials_pointers, 
						NEUTRAL_SENTENCE : neus_pointers, 
						NEGATIVE_SENTENCE: negs_pointers}
		trials = [] + [practice]*self.n_practice_trials + [neu]*self.n_start_neutral_trials + trials
		
		# Adding sentences to the TrialType instances
		for p in prac_neu_or_neg[NEGATIVE_SENTENCE]:
			neg.add_sentence(self.neg_sentences_by_phase[phase][p])
		
		for p in prac_neu_or_neg[NEUTRAL_SENTENCE]:
			neu.add_sentence(self.neu_sentences_by_phase[phase][p])
		
		for sentence in practice_trials_sentences:
			practice.add_sentence(sentence)
		
		ammount_of_neutral_trials = len(neu.sentences) # saving a reffernce to the ammount of neutral setnences
		
		
		# saving final values:
		self.sentences_instances_by_type_by_phase[phase] = {
															neu: self.neu_sentences_by_phase[phase], 
															neg: self.neg_sentences_by_phase[phase], 
															practice: practice_trials_sentences
															}
		self.trials_types_by_phase[phase] = trials
		
		# re arranging trial types according to AFACT demands:
		if phase == AFACT_PHASE:
			self._afact_trials_rearrange(phase, ammount_of_neutral_trials, prac_neu_or_neg, neu, neg)
		
		elif phase == DICHOTIC_PHASE:
			pass
			
	def _afact_trials_rearrange(self, phase, 
								ammount_of_neutral_trials, 
								prac_neu_or_neg, 
								neu, neg):
		'''
			This function is executed only if phase is sepcfied exactly as
			AFACT_PHASE. Then, it rearranges the trials to follow the rule of
			a neg followed by concecutive one or two ntrs
			
		'''
		# index of sentences to rearrage	
		i_to_rearrange = self.n_start_neutral_trials + self.n_practice_trials

		#		The following dubles by 1.5 the ammount of neutral trials, this to sumulate
		# 	a random choise of either 1 or 2 consecutive trials after an ntr
		half_ammount_of_ntrs = int(round(ammount_of_neutral_trials/2.0))
		additional_pointers = random.sample(prac_neu_or_neg[NEUTRAL_SENTENCE], half_ammount_of_ntrs)
		random.shuffle(additional_pointers) # to avoid consectuive is not mixed with the rest of trials
		prac_neu_or_neg[NEUTRAL_SENTENCE] = additional_pointers + prac_neu_or_neg[NEUTRAL_SENTENCE]
		
		# smpelinG initial ntr trials pointer to be added IN FEW LINES AHEAD
		neu.sentences = []  # deleting existing sentences
		neus_pointers = range(len(self.neu_sentences_by_phase[phase]))
		ntr_pointers_for_initial_trials = random.sample(neus_pointers, self.n_start_neutral_trials)
		# in afact beacuse every neg trials follows by additional 1-2 ntr, the initial windows should be additional
		for p in ntr_pointers_for_initial_trials:
			neu.add_sentence(self.neu_sentences_by_phase[phase][p])
		# all rest ntr trials
		for p in prac_neu_or_neg[NEUTRAL_SENTENCE]:
			neu.add_sentence(self.neu_sentences_by_phase[phase][p])
		
		cons = [1]*half_ammount_of_ntrs + [2]*half_ammount_of_ntrs
		random.shuffle(cons)
		
		# ensuring negs always followed by 1 or 2 ntr:
		trials = []
		for c in cons:
			trials.append(neg)
			trials = trials + [neu]*c
			
		# saving afact trials
		self.trials_types_by_phase[phase] = self.trials_types_by_phase[phase][:i_to_rearrange] + trials
	
	def fill_sentence_trial_refferences(self):
		for phase in self.phases_names:
			self.sentence_trial_reffs_by_phase[phase] = TrialsSentencesReff()
			trial_types = self.trials_types_by_phase[phase]
			unique_types_reff = np.unique(trial_types)
			for trial in trial_types:
				self.sentence_trial_reffs_by_phase[phase].sentences_instances.append(trial.sentences[trial.index])
				trial.index += 1
			
			# reseting indexes back on 0
			for unique_trialtype in unique_types_reff:
				unique_trialtype.index = 0
				
	def define_change_block_trials_per_phase(self):
		for phase in self.trials_types_by_phase:
			if self.n_block_per_phase[phase] > 1: 
				trials = self.trials_types_by_phase[phase]
				change_block_trial = int(round((len(trials)-1)/2.0))
				# following lines asures that change block trial type wouldn't be 
				# 	before feedback or catch.
				correction_counter = 0
				while not trials[change_block_trial+correction_counter].is_normal_trial: #
					correction_counter+=1
				change_block_trial += correction_counter
				
				# saving a reff of final change block trial number
				self.change_block_trials_by_phase[phase] = change_block_trial
				
				change_block_trial_type = TrialType("Change_Block")
				change_block_trial_type.is_normal_trial = False
				change_block_trial_type.is_change_block_trial = True
				trials.insert(change_block_trial, change_block_trial_type)
				
	def insert_feedback_trialtypes_on_afact_phase(self):
		if self.afact_phase in self.trials_types_by_phase:
			afact_trials = self.trials_types_by_phase[self.afact_phase]
			for i, trial in enumerate(afact_trials):
				if trial.type == NEGATIVE_SENTENCE:
					feedback_trial_type = TrialType("afact_feedback Trial")
					afact_trials.insert(i+1, feedback_trial_type)
					afbt = afact_trials[i+1]
					afbt.is_afact_feedback = True
					afbt.is_normal_trial = False
		else:
			# No afact phase on this instance
			pass
		
		
	def insert_catch_trials_trial_types(self):
		for phase in self.phases_names:
			catch_trials_insertion_counter = 0 # makes sure that pushing (insert) catch trials into the list in 
										# in various i's (in the following for) is aimed at the original place
			for i, trial in enumerate(self.catch_and_non_catch_trials_list_by_phase[phase]):
				if trial !=0:
					# pushing catch trials to their location on the phase trials
					catch = TrialType("{}-Catch Trial".format(trial))
					self.trials_types_by_phase[phase].insert(i+catch_trials_insertion_counter, catch)
					catch_trials_insertion_counter += 1
					# giving each catch its functionality
					sentences_scope_until_this_catch = self.sentence_trial_reffs_by_phase[phase].sentences_instances[:i] # excluding this catch
					catch.is_catch = True
					catch.is_normal_trial = False
					if trial == "c":
						sentence = sentences_scope_until_this_catch[-1] # chosing last sentence
						catch.catch_type = True # correct catch
					elif trial == "w":	
						sentence = random.sample(sentences_scope_until_this_catch[:-1], 1)[0] # excluding the last one
						catch.catch_type = False # wrong catch
					# saving sentence text and num
					catch.catch_sentence = sentence
						
	def create_catch_trials(self):
		for phase in self.phases_names:
			if not phase in self.phases_without_catch_trials:
				trials = len(self.trials_types_by_phase[phase]) - self.n_practice_trials - self.n_start_neutral_trials
				number_of_catch_trials = int(self.precent_of_catch_trials*trials)
				corrects = int(number_of_catch_trials/2.0)
				wrongs = number_of_catch_trials - corrects
				cs = ['c']*corrects
				ws = ['w']*wrongs
				non_catch_trials = [0]*(trials-number_of_catch_trials)
				all_trials =  cs + ws + non_catch_trials
				random.shuffle(all_trials)
				
				while not self._check_no_consecutive_trials(all_trials):
					# fixing to close catches:
					all_trials = self._fix_consecutive_trials(all_trials)
				
				all_trials = [] + self.n_practice_trials*[0] + self.n_start_neutral_trials*[0] + all_trials
				
				self.catch_and_non_catch_trials_list_by_phase[phase] = all_trials	
	
	def _fix_consecutive_trials(self, all_trials):
		for i, t in enumerate(all_trials): 
			if i>0:
				if t!=0: # t is a catch trial
					if all_trials[i-1] != 0:
						t_to_trnasfer = all_trials.pop(i) # delete and grab to transfer
						new_i = random.randint(1,len(all_trials)-2)
						while all_trials[new_i-1] != 0 or all_trials[new_i] !=0:
							new_i = random.randint(1,len(all_trials)-2)
						all_trials.insert(new_i, t_to_trnasfer)
		return all_trials
	
	def _check_no_consecutive_trials(self, all_trials):
		# add practice non-catch trials in the begining
		counter = 0
		for i in range(len(all_trials)): 
			if all_trials[i] !=0: 
				if i+1 != len(all_trials):
					if all_trials[i+1] != 0:
						counter += 1
		if counter == 0:
			return True
		else:
			return False
		
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


class TrialsSentencesReff(object):
	'''
		A class that helps keep tracking on sentneces instances that appearded on each trial across trials types
	'''
	def __init__(self):
		self.sentences_instances = []
		
	def find_sentence_by_trial(self, trial):
		return self.sentences_instances[trial]


class TrialType(object):
	def __init__(self, type):
		self.type = type
		self.index = 0
		self.sentences = []
		
		# trial type boolean
		self.is_normal_trial 		= 	True
		self.is_change_block_trial 	= 	False
		self.is_afact_feedback 		= 	False
		self.is_catch 				=	False 
		self.is_practice 			=	False # Can be True alogside is_normal_trial=True
		
		# only for catch trials - True=Correct, False=Wrong sentence on catch
		self.catch_sentence = None
		self.catch_type = None # manulally changes to true or false in creation
	
	def add_sentence(self, sentence):
		self.sentences.append(sentence)
		
	def get_current_sentence(self):
		if self.is_normal_trial:
			return self.sentences[self.index]
		elif self.is_catch:
			return self.catch_sentence
			

	def next(self):
		if self.index < len(self.sentences)-1: # holding index on the last sentence
			self.index += 1
			
	def __str__(self):
		return 'TrialType {}'.format(self.type)
		
	def __repr__(self):
		return self.__str__()
	

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

	def __str__(self):
		return 'Sentence {} - {}'.format(self.valence, str(self.num))
		
	def __repr__(self):
		return self.__str__()
		
		