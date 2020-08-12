import pandas as pd
import os
import random
import ipdb
import copy
import numpy as np

from ..params import *

class MainAudioProcessor(object):
	
	def __init__(self, 
						phases_names=None, 
						n_start_neutral_trials =None, 
						n_trials_by_phase=None, 
						n_practice_trials=None, 
						pre_defined_distribution_dict=None, 
						precent_of_catch_trials=None, 
						phases_without_catch_trials=None,
						n_block_per_phase=None,
						dichotic_phases=None,
						phases_relations=None,
						afact_debug=False,
						):
						
		self.phases_names = phases_names # A list of strings representing phases names
		self.n_phases = len(self.phases_names) # Ammount of experimentatl phases to split sentence to
		self.n_trials_by_phase = n_trials_by_phase # ammount of trials per phase - a dictionary -  determines how many sentence repetition should occur
		self.afact_phase = AFACT_PHASE
		self.dichotic_phases = dichotic_phases
		self.phases_relations = phases_relations				
		self.first_phase = DIGIT_PRE
		self.afact_debug = afact_debug

		if n_practice_trials == None:
			self.n_practice_trials= DEFAULT_N_PRACTICE_TRIALS
		else:
			self.n_practice_trials = n_practice_trials
		
		if precent_of_catch_trials==None:
			self.precent_of_catch_trials = DEFAULT_CATCH_TRIALS_RATIO
		else:
			self.precent_of_catch_trials = precent_of_catch_trials
		
		if n_start_neutral_trials==None:
			self.n_start_neutral_trials = DEFAULT_N_START_NEUTRAL_TRIALS # real data trials
		else:
			self.n_start_neutral_trials = n_start_neutral_trials
		
		if phases_without_catch_trials==None:
			self.phases_without_catch_trials = [] # means that all phases needs catch trials
		else:
			self.phases_without_catch_trials = phases_without_catch_trials
			
		if n_block_per_phase==None:
			self.n_block_per_phase = {} # means that all phases have two blocks
			for phase in self.phases_names:
				self.n_block_per_phase[phase] = DEFAULT_N_BLOCK_PER_PHASE
		else:
			self.n_block_per_phase = n_block_per_phase 
			for phase in self.phases_names:
				if not phase in self.n_block_per_phase:
					self.n_block_per_phase[phase] = DEFAULT_N_BLOCK_PER_PHASE # means that all phases that where not specified, are of two phases

		# if False:
		# 	if self.dichotic_phases != None: # a dichotic task is requested by user
		# 		for dichotic_phase in self.dichotic_phases:
		# 			self.n_dichotic_trials = self.n_trials_by_phase[dichotic_phase] # saving a refference to the requsted n
		# 			# removing dichotic from lists and dicts that are unrelevant for further process
		# 			self.phases_names.remove(dichotic_phase)
		# 			self.n_trials_by_phase.pop(dichotic_phase, None)
			
		
		self.pre_defined_distribution_dict = pre_defined_distribution_dict
		
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
		self.sentences_by_phase = {} # sentences by phase 
		
		self.trials_types_by_phase = {} #  per phase, list of TYPES as strings "ntr", "neg" or "prac"
		self.sentences_instances_by_type_by_phase = {} # per phase, with index and type, SENTNECE INSTANCE
		self.sentence_trial_reffs_by_phase = {} # contains TrialsSentencesReff instances by phase
		self.change_block_trials_by_phase = {} # each phase change block trial refference

		self.process_sentences_data() # sentence are read from excel and located at dir an classified by valence *HERE PRE LOAD SHOULD HAPPEN*
		self._split_senteces_to_phases()
		self._create_trials_pointers_by_phase()
		self.create_catch_trials()
		self.fill_sentence_trial_refferences()
		if not self.afact_debug:
			self.insert_catch_trials_trial_types()
		self.insert_feedback_trialtypes_on_afact_phase()
		self.define_change_block_trials_per_phase()
		self.insert_instructions_trial_types()

		self.debug_trials()

	def debug_trials(self):
		dubg_data = {"Sentence":[], "Phase":[]}
		for phase in self.trials_types_by_phase:
			trial_type_counter = {}
			sents = []
			for trial_type in self.trials_types_by_phase[phase]:
				trial_type_name = trial_type.__str__()
				trial_type_counter.setdefault(trial_type_name, 0)
				if len(trial_type.sentences) > 0 :
					sents.append(trial_type.sentences[trial_type_counter[trial_type_name]])
					trial_type_counter[trial_type_name] += 1

			dubg_data["Sentence"] = dubg_data["Sentence"] + sents
			dubg_data["Phase"] = dubg_data["Phase"] + [phase]*len(sents)

		df = pd.DataFrame(dubg_data)
		df.to_excel(r".\\Debug Output\\dubg_trials.xlsx", index=False)



	def _split_senteces_to_phases(self):
		'''the function gets a matrix for sentecnes per task and phase, and 80 subject data,
			and allocate the sentences for each session'''

		SUBJECT_AUDIO_DATA = self.audio_path + '\\' + r'audio_data.xlsx'
		if self.menu.menu_data["session"] != 2:
			#read files
			subject_data = pd.read_excel(SUBJECT_AUDIO_DATA)
			allocation_plan = pd.read_excel(ALLOCATION)

			data_neg = subject_data[subject_data['SentenceType'] == 'neg']
			data_ntr = subject_data[subject_data['SentenceType'] == 'ntr']

			dic_phases_number = {}

			if ALLOCATION == ALLOCATION_OMER:
				#read allocation plan
				Digit_before = allocation_plan.iloc[0, 2]
				Digit_after = allocation_plan.iloc[0, 3]
				Digit_before_after = allocation_plan.iloc[0, 4]

				Dichotic_before = allocation_plan.iloc[1, 2]
				Dichotic_after = allocation_plan.iloc[1, 3]
				Dichotic_before_after = allocation_plan.iloc[1, 4]
				#split data to neg/neu
				n_list= [Digit_before, Digit_after, Dichotic_before, Dichotic_after, Digit_before_after, Dichotic_before_after]
				# Dependent on the "Sentences_Allocation_Omer.xlsx" that sitts in -> r"stp-project\Tasks\processing"
				n_str_list = self.phases_names + ['Digit_before_after', 'Dichotic_before_after'] # adding only those with before and after

			else: # Allocation Tomer
				Digit_before            = allocation_plan.iloc[0, 2]
				Digit_after             = allocation_plan.iloc[1, 2]
				AFACT		        	= allocation_plan.iloc[2, 2]
				MAB 		        	= allocation_plan.iloc[3, 2]
				Dichotic		        = allocation_plan.iloc[4, 2]
				Digit_before_and_AFACT  = allocation_plan.iloc[2, 3]
				MAB_and_AFACT           = allocation_plan.iloc[3, 4]
				MAB_and_Digit_after     = allocation_plan.iloc[3, 5]
				Dichotic_and_AFACT      = allocation_plan.iloc[4, 4]

				n_list= [
					Digit_before,
					Digit_after,
					AFACT,
					MAB,
					Dichotic,
					Digit_before_and_AFACT,
					MAB_and_AFACT,
					MAB_and_Digit_after,
					Dichotic_and_AFACT,
				] # Dependent on the "Sentences_Allocation_Omer.xlsx" that sitts in -> r"stp-project\Tasks\processing"
				n_str_list = self.phases_names + [
					"Digit_before_and_AFACT",
					"MAB_and_AFACT",
					"MAB_and_Digit_after",
					"Dichotic_and_AFACT",
				] # adding only those with before and after

			for i in range(len(n_list)):
				dic_phases_number[n_str_list[i]]= n_list[i]

			for data in [data_neg, data_ntr]:
				index_list = list(data.index) #[0,...,39] / [40,...79]
				for k in dic_phases_number.keys():
					sample_index_list = random.sample(index_list, int(dic_phases_number[k]))
					for i in sample_index_list:
						index_list.remove(i)
						subject_data.at[i, 'Phases'] = k

			subject_data.to_excel(SUBJECT_AUDIO_DATA, index=False)

		else:
			subject_data = pd.read_excel(SUBJECT_AUDIO_DATA)

		################################# Runs in Session one and two (Omer) #################################
		sentence_valence_dicts = {'ntr': self.neu_sentences_by_phase, 'neg': self.neg_sentences_by_phase}

		for sentence in self.sentences:
			sentence_phase = subject_data.loc[subject_data["TAPlistNumber"]==sentence.num_in_excel, "Phases"].values[0]
			if sentence_phase in self.phases_relations:
				# a sentence that repeats on before and after
				for phase in self.phases_relations[sentence_phase]:
					self.sentences_by_phase.setdefault(phase, []).append(sentence)
					sentence_valence_dicts[sentence.valence].setdefault(phase, []).append(sentence)
			else:
				# an exclusive by phase and task sentence
				self.sentences_by_phase.setdefault(sentence_phase, []).append(sentence)
				sentence_valence_dicts[sentence.valence].setdefault(sentence_phase, []).append(sentence)

		# AT this point i have unique neus and negs per phase

	def _create_trials_pointers_by_phase(self):
		for phase in self.phases_names:
			if phase not in self.dichotic_phases: # skipps dichitc because it has its own way of handeling trials
				# rounded_multplying_factor by using it I know how many repetition per sentence
				ammount_unique_sentences = len(self.sentences_by_phase[phase])
				rounded_multplying_factor = int(round(1.0*self.n_trials_by_phase[phase]/ammount_unique_sentences))
				# creating intial pointers
				neus_pointers = list(range(len(self.neu_sentences_by_phase[phase])))
				negs_pointers = list(range(len(self.neg_sentences_by_phase[phase])))
				# Adding practice trials --> cuurently multplying existing neutrasl
				practice_trials_pointers = random.sample(self.neutral_sentences, self.n_practice_trials) # 8 is the default number of practice trials
				# first shuffeling of originals:
				random.shuffle(neus_pointers)
				random.shuffle(negs_pointers)
				
				# creating additional pointers to fit desired amount of trials
				lists_of_additional_neus_pointers = []
				lists_of_additional_negs_pointers = []
				ammount_of_additions = rounded_multplying_factor-1
				for i in list(range(ammount_of_additions)):
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
				PRACTICE_SENTENCE = "prac_1"
				PRACTICE_SENTENCE_2 = "prac_2"
				
				neu = TrialType(NEUTRAL_SENTENCE)
				neg = TrialType(NEGATIVE_SENTENCE)
				practice_1 = TrialType(PRACTICE_SENTENCE)
				practice_2 = TrialType(PRACTICE_SENTENCE_2)
				
				practice_1.is_practice = True # Controls for feedback -  on prac 1 --> providing feedback
				practice_1.trial_phase = "practice 1"
				practice_2.is_practice = False # Controls for feedback -  on prac 2 --> no feedback
				practice_2.trial_phase = "practice 2"
				
				
				# arranging trials:
				trials = [neu]*(len(neus_pointers)-self.n_start_neutral_trials) + [neg]*len(negs_pointers) # - n_start_neutral_trials is for the intial four neus to be later added
				random.shuffle(trials)
				
				# creating new instances with deep copy for practice trials
				practice_trials_sentences = [] + practice_trials_pointers
				
				
				prac_neu_or_neg = {
								PRACTICE_SENTENCE: practice_trials_pointers, 
								NEUTRAL_SENTENCE : neus_pointers, 
								NEGATIVE_SENTENCE: negs_pointers}
				
				# Adding sentences to the TrialType instances
				for p in prac_neu_or_neg[NEGATIVE_SENTENCE]:
					neg.add_sentence(self.neg_sentences_by_phase[phase][p])
				
				for p in prac_neu_or_neg[NEUTRAL_SENTENCE]:
					neu.add_sentence(self.neu_sentences_by_phase[phase][p])
				
				for i, sentence in enumerate(practice_trials_sentences):
					if i < self.n_practice_trials/2:
						practice_1.add_sentence(sentence)
					else:
						practice_2.add_sentence(sentence)
				
				ammount_of_neutral_trials = len(neu.sentences) # saving a reffernce to the ammount of neutral setnences
				
				trials = [] + [practice_1]*len(practice_1.sentences) + [practice_2]*len(practice_2.sentences) + [neu]*self.n_start_neutral_trials + trials
				
				# saving final values:
				self.sentences_instances_by_type_by_phase[phase] = {
																	neu: self.neu_sentences_by_phase[phase], 
																	neg: self.neg_sentences_by_phase[phase], 
																	practice_1: practice_1.sentences,
																	practice_2: practice_2.sentences
																	}
				self.trials_types_by_phase[phase] = trials
				
				# re arranging trial types according to AFACT demands:
				if phase == AFACT_PHASE:
					self._afact_trials_rearrange(phase, ammount_of_neutral_trials, prac_neu_or_neg, neu, neg)
				
				elif phase == DICHOTIC_PHASE:
				#OMER
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
		
		# smpeling initial ntr trials pointers to be added IN FEW LINES AHEAD
		neu.sentences = []  # deleting existing sentences
		neus_pointers = list(range(len(self.neu_sentences_by_phase[phase])))
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
			if phase not in self.dichotic_phases:
				self.sentence_trial_reffs_by_phase[phase] = TrialsSentencesReff()
				trial_types = self.trials_types_by_phase[phase]	 
				unique_types_reff = pd.Series(trial_types).unique()
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
				change_block_trial = self.n_practice_trials + int(round((len(trials)-1 - self.n_practice_trials)/2.0))
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
			print(phase)
			catch_trials_insertion_counter = 0 # makes sure that pushing (insert) catch trials into the list in 
			if not phase in self.phases_without_catch_trials:							# in various i's (in the following for) is aimed at the original place
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
						
						# adding practice catch trials
				index_practice_2_strat_trial = int(self.n_practice_trials*0.75)
				index_practice_2_end_trial = self.n_practice_trials
				practice_with_catch = list(range(index_practice_2_strat_trial, index_practice_2_end_trial))
				catch_counter = 0
				
				for i, prac_catch_index in enumerate(practice_with_catch):
					catch = TrialType("prac_{}-Catch Trial".format(str(prac_catch_index+1)))
					catch.is_catch = True
					catch.is_normal_trial = False
					self.trials_types_by_phase[phase].insert(prac_catch_index+1+catch_counter, catch)
					# Ctach sentence is currently always the one before catch trials - thus always correct
					catch_sentence = self.trials_types_by_phase[phase][prac_catch_index+catch_counter].sentences[i + 2] # first two sentences of practice two have no catch
					catch.catch_type = True # stands for correct catch trials
					
					self.trials_types_by_phase[phase][prac_catch_index+1+catch_counter].catch_sentence = catch_sentence
					
					catch_counter += 1
						
	def insert_instructions_trial_types(self):
		# absolute numbers of instructions that build on 8 practice trials
		# see constants above
		instructions = TrialType("Instructions")
		instructions.is_normal_trial = False
		instructions.is_instructions = True
		self.trials_types_by_phase[self.first_phase].insert(AFTER_PRACTICE_1, instructions)
		self.trials_types_by_phase[self.first_phase].insert(AFTER_PRACTICE_2, instructions)
						
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
		for i in list(range(len(all_trials))): 
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
		
		for i in list(range(len(self.audio_df))):
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
		self.trial_phase 			=   "Real Trial"
		self.is_normal_trial 		= 	True
		self.is_change_block_trial 	= 	False
		self.is_afact_feedback 		= 	False
		self.is_catch 				=	False 
		self.is_practice 			=	False # Can be True alogside is_normal_trial=True
		self.is_instructions = False
		
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
		self.text = u"" + text
		self.valence = valence
		self.num = num
		self.num_in_excel = num_in_excel
		self.file_path = file_path
		self.sentence_length = sentence_length*ONE_SECOND # in miliseconds
		self.digit_que = int(self.sentence_length-MILISECONDS_BEFORE_END) # time of sentence start
		self.is_practice = False
		

	def __str__(self):
		return 'Sentence {} - {}'.format(self.valence, str(self.num))
		
	def __repr__(self):
		return self.__str__()
		