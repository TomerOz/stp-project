import pandas as pd
import os
import random
import ipdb
import copy

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
	
	def __init__(self, phases_names=None, n_trials_by_phase=None, n_practice_trials=None, phases_distribution_percent_dict=None, precent_of_catch_trials=None):
		
		self.phases_names = phases_names # A list of strings representing phases names
		self.n_phases = len(self.phases_names) # Ammount of experimentatl phases to split sentence to
		self.n_trials_by_phase = n_trials_by_phase # ammount of trials per phase - a dictionary -  determines how many sentence repetition should occur

		if n_practice_trials == None:
			self.n_practice_trials=8
		else:
			self.n_practice_trials = n_practice_trials
		
		if precent_of_catch_trials==None:
			self.precent_of_catch_trials = 3.0/8.0
		else:
			self.precent_of_catch_trials = precent_of_catch_trials
		
		self.n_start_neutral_trials = 4 # real data trials
		self.phases_distribution_percent_dict = phases_distribution_percent_dict
	
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

		self.process_sentences_data() # sentence are read from excel and located at dir an classified by valence *HERE PRE LOAD SHOULD HAPPEN*
		self._split_senteces_to_phases()
		self.create_catch_trials()
		
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
		neus_pointers = range(len(self.neu_sentences_by_phase[phase]))*rounded_multplying_factor # pointers of neutral sentences
		negs_pointers = range(len(self.neg_sentences_by_phase[phase]))*rounded_multplying_factor # Ipointers of neutralnegative sentences
		
		# Checking if multiplying reached the desired ammount of trials
		if len(neus_pointers)*2 < self.n_trials_by_phase[phase]:
			delta = int(round((self.n_trials_by_phase[phase] - len(neus_pointers)*2)/2.0))
			neu_additional_pointers = random.sample(neus_pointers,delta)
			neg_additional_pointers = random.sample(negs_pointers,delta)
			neus_pointers = neus_pointers + neu_additional_pointers
			negs_pointers = negs_pointers + neg_additional_pointers	
			
		ammount_of_trials = len(neus_pointers) + len(negs_pointers) # Int number of total ammunt of trials
		# shuffeling:
		random.shuffle(neus_pointers)
		random.shuffle(negs_pointers)
		# creating an all trials dictionary
		PRACTICE_SENTENCE = "prac"
		sents_by_trials = TrialsSentencesReff()
		neu = TrialType(NEUTRAL_SENTENCE, sents_by_trials)
		neg = TrialType(NEGATIVE_SENTENCE, sents_by_trials)
		practice = TrialType(PRACTICE_SENTENCE, sents_by_trials)
		# arranging trials:
		trials = [neu]*(len(neus_pointers)-self.n_start_neutral_trials) + [neg]*len(negs_pointers) # - n_start_neutral_trials is for the intial four neus to be later added
		random.shuffle(trials)
		
		# Adding practice trials --> cuurently multplying existing neutrasl
		practice_trials_pointers = random.sample(neus_pointers, self.n_practice_trials) # 8 is the default number of practice trials
		
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
		
		neu.sentences = []  # deleting existing sentences
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
		
	def create_catch_trials(self):
		for phase in self.phases_names:
			trials = len(self.trials_types_by_phase[phase]) - self.n_practice_trials
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
		
			### AND ----> ADAPT THE DCT TASK - CHANGE IT IN GENERAL TO BE BETTER
	
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
	def __init__(self, type, trial_sent_ref):
		self.type = type
		self.trial_sent_ref = trial_sent_ref
		self.index = 0
		self.sentences = []
		
	def add_sentence(self, sentence):
		self.sentences.append(sentence)
		
	def get_current_sentence(self):
		return self.sentences[self.index]
	
	def next(self):
		self.save_sentnece_and_trial() # keep tracking on which sentnece was heared on which trial
		if self.index < len(self.sentences)-1: # holding index on the last sentence
			self.index += 1
		print self.trial_sent_ref.sentences_instances
	def save_sentnece_and_trial(self):
		self.trial_sent_ref.sentences_instances.append(self.sentences[self.index])
		
		
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
		return 'Sentence {}'.format(self.valence)
		
	def __repr__(self):
		return self.__str__()
		
		