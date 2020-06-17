import os
import pandas as pd
import time
import ipdb


#to params
#builds on the response key to be right/left arrows.
DICHOTIC_LEFT_KEYSYM = 'Left'
DICHOTIC_RIGHT_KEYSYM = 'Right'

class SubjectData(object):

	def __init__(self, full_data_path=""):
	
		self.full_data_path = full_data_path
		
		self.subject_col = []
		self.gender_col = []
		self.group_col = []
		self.session_col = []
		
		self.trials_nums = []
		self.trials_types = [] # catch or (relase LOL) normal
		self.blocks = []
		self.categorization_scores = [] # 0 or 1
		self.pressed_keys = [] # l or r
		self.RTs = []
		self.nums_shown_types = []
		self.catch_trial_types = []
		self.sentence_instances = [] # valence, text, path, duration etc....
		self.experimental_phase = []
		self.trials_phases = [] # practice or real trials
		
		# unpacked sentence properties:
		self.sentences_valence = []
		self.sentences_texts = []
		self.sentences_nums = []
		self.sentences_duration = []
		self.sentences_paths = []
		
	def add_menu_data(self, subject, group, gender, session):
		self.subject = subject
		self.gender = gender
		self.group = group
		self.session = session
			
	def push_data_packge(self, package):
		recorded_trial = package.current_trial-1
		sentence = package.current_sentence 
		
		block = package.current_block
		trial_type = self._classify_trial(package.is_catch_trial)
		
		
		last_key = package.last_key_pressed # last key press
		was_correct = package.last_trial_classification # was last trial correct or not
		last_rt = package.last_RT # last trial rt
		num_shown_type = package.num_shown_type
		phase = package.phase
		
		self.trials_nums.append(recorded_trial)
		self.trials_types.append(trial_type)
		self.blocks.append(block)
		self.categorization_scores.append(was_correct)
		self.pressed_keys.append(last_key)
		self.RTs.append(last_rt)
		self.nums_shown_types.append(num_shown_type)
		self.experimental_phase.append(phase)
		self.subject_col.append(self.subject)
		self.gender_col.append(self.gender)
		self.group_col.append(self.group)
		self.session_col.append(self.session)
		
		self.trials_phases.append(package.trial_phase)
		
		
		
		if trial_type == 'catch':
			self.catch_trial_types.append(package.correct)
		else:
			self.catch_trial_types.append('not_catch')
		
		self.sentence_instances.append(sentence)
		self.unpack_sentences_data(sentence)
			
	def _classify_trial(self, is_catch_trial):
		if is_catch_trial:
			return 'catch'
		else:
			return 'normal'
	
	def unpack_sentences_data(self, sentence_instance):
		valence = sentence_instance.valence
		num =  sentence_instance.num
		file_path =  sentence_instance.file_path
		sentence_length =  sentence_instance.sentence_length
		text =  sentence_instance.text
		
		self.sentences_valence.append(valence)
		self.sentences_texts.append(text)
		self.sentences_duration.append(sentence_length)
		self.sentences_paths.append(file_path)
		self.sentences_nums.append(num)
				
	def create_data_frame(self):
		subject_df = pd.DataFrame()
		
		columns = ['subject', 'trial num', 'experimental_phase', 'trial type', 'catch trial type',
					'block', 'is correct', 'key pressed', 'RT', 'valence',
					'text', 'duration', 'path', 'sentence num',
					'num shown', 'gender', 'group', 'session', 'trials_phases']
					
		rows = [
					self.subject_col			,
					self.trials_nums			,
					self.experimental_phase		,
					self.trials_types			,
					self.catch_trial_types      ,
					self.blocks					,
					self.categorization_scores	,
					self.pressed_keys			,
					self.RTs					,
					self.sentences_valence		,
					self.sentences_texts		,
					self.sentences_duration		,
					self.sentences_paths		,
					self.sentences_nums			,
					self.nums_shown_types		,
					self.gender_col				,
					self.group_col				,
					self.session_col			,
					self.trials_phases			,
				]
				
		for i,r in enumerate(rows):
			subject_df[columns[i]] = pd.Series(r)
		
		subject_dir = os.path.join(self.full_data_path, r'Data\Subject_' + self.experimental_phase[0] + '_' + str(self.subject))
		if not os.path.exists(subject_dir):
			os.mkdir(subject_dir) 
		subject_df.to_excel(subject_dir + '\\data.xlsx')
		return subject_df
			
			
class DichoticSubjectData(object):
	def __init__(self):
		
		self.trial_side 			= []
		self.trial_number			= []
		self.trial_phase 			= []
		self.trial_valence 			= []
		self.trial_start_time 		= []
		self.trial_end_time 		= []
		self.sentences_durations 	= []
		self.subject 				= []
		self.gender 				= []
		self.group				 	= []
		self.session			 	= []
		self.blocks				 	= []
		self.sentence_ids			= []

		# Currently not parrt of DF - that is for uncertainty regarding their length (multiple presses are allowed)
		self.trial_response = []
		self.trial_response_time = []
	
	def create_df(self):
		
		columns = [
					"trial_side",
					"trial_number",
					"trial_phase",
					"trial_valence",
					"trial_start_time",
					"trial_end_time",
					"sentences_durations",
					"subject",
					"gender",
					"group",
					"session",
					"block",
					"sentence_id",
					]

		rows = [
				self.trial_side 		,
				self.trial_number		,
				self.trial_phase 		,
				self.trial_valence 		,
				self.trial_start_time 	,
				self.trial_end_time 	,
				self.sentences_durations,
				self.subject			,
				self.gender          	,
				self.group	            ,
				self.session            ,
				self.blocks	            ,
				self.sentence_ids	    ,
				]

		df = create_generic_row_cols_data_frame(rows, columns, r'Data\Subject_' + str(self.subject[0]), "Dichotic")
		self.insert_responses(df)
	
	def insert_responses(self, df):
		
		df["Response_Left"] = False
		df["Response_Left_time"] = False
		df["Response_Right"] = False
		df["Response_Right_time"] = False
		
		# Adding time stamp and pressed key on the intersection between trial start and end that corresponds to the time stamp
		for i, response_t in enumerate(self.trial_response_time):
			response_key = self.trial_response[i]
			if response_key == DICHOTIC_LEFT_KEYSYM: 
				df.loc[(df.trial_start_time<=response_t) & (df.trial_end_time>=response_t), "Response_Left"] = response_key
				df.loc[(df.trial_start_time<=response_t) & (df.trial_end_time>=response_t), "Response_Left_time"] = response_t
			elif response_key == DICHOTIC_RIGHT_KEYSYM:
				df.loc[(df.trial_start_time<=response_t) & (df.trial_end_time>=response_t), "Response_Right"] = response_key
				df.loc[(df.trial_start_time<=response_t) & (df.trial_end_time>=response_t), "Response_Right_time"] = response_t
				
				
		df.to_excel(r'Data\Subject_' + str(self.subject[0]) + "\\Dichotic.xlsx")

	def get_response(self, event=None):
		self.trial_response_time.append(time.time())
		self.trial_response.append(event.keysym)
	
	def record_trial(self, td, channel=None):
		if td.task_phase == "First Practice":
			side = td.practice_one_side
			trial_number = td.practice_trial
			sentence = td.current_practice_sentence 
			start_t = td.practice_1_strat_time
			end_t = td.practice_1_end_time
			
		elif td.task_phase == "Second Practice":
			side = channel
			if channel == "Right":
				trial_number = td.practice_trial_right
				sentence = td.current_prac_right_sentence
				start_t = td.practice_2_right_start_time
				end_t = td.practice_2_right_end_time
			elif channel == "Left":
				trial_number = td.practice_trial_left
				sentence = td.current_prac_left_sentence
				start_t = td.practice_2_left_start_time 
				end_t = td.practice_2_left_end_time	
			
		elif td.task_phase == "Real Trials":
			valence_side_keys_list = [*td.valence_side.keys()]
			valence_side_values_list = [*td.valence_side.values()]
			side = valence_side_keys_list[valence_side_values_list.index(channel)]
			
			if channel == "neu":
				trial_number = td.neu_trial
				sentence = td.current_neu_sentence
				start_t = td.real_trials_neu_start_time
				end_t = td.real_trials_neu_end_time
			elif channel == "neg":
				trial_number = td.neg_trial
				sentence = td.current_neg_sentence
				start_t = td.real_trials_neg_start_time 
				end_t = td.real_trials_neg_end_time
		
		self.trial_side				.append(side)
		self.trial_number			.append(trial_number)
		self.trial_phase			.append(td.task_phase)
		self.trial_valence			.append(sentence.valence)
		self.trial_start_time		.append(start_t)
		self.trial_end_time         .append(end_t)
		self.sentences_durations	.append(sentence.sentence_length)
		self.subject				.append(td.subject)
		self.gender					.append(td.gender)
		self.group					.append(td.group)
		self.session				.append(td.session)
		self.blocks					.append(td.block)
		self.sentence_ids			.append(sentence.num)

def create_generic_row_cols_data_frame(rows, cols, destination, file_name):
		subject_df = pd.DataFrame()
		for i,r in enumerate(rows):
			subject_df[cols[i]] = pd.Series(r)
		
		subject_dir = os.path.join(destination)
		if not os.path.exists(subject_dir):
			os.mkdir(subject_dir) 
		subject_df.to_excel(subject_dir + '\\' + file_name + '.xlsx')
		return subject_df
	