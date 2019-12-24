import os
import pandas as pd

class SubjectData(object):
	
	def __init__(self):
	
		self.subject_col = []
		self.gender_col = []
		self.group_col = []
		
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
		
		# unpacked sentence properties:
		self.sentences_valence = []
		self.sentences_texts = []
		self.sentences_nums = []
		self.sentences_duration = []
		self.sentences_paths = []
		
	def add_menu_data(self, subject, group, gender):
		self.subject = subject
		self.gender = gender
		self.group = group
		
	
	def push_data_packge(self, package):
		recorded_trial = package.current_trial-1
		sentence = package.sentences[package.current_trial - 2] # see scheme to understand whay I'm taking to steps back
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
					'num shown', 'gender', 'group']
					
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
				]
				
		for i,r in enumerate(rows):
			subject_df[columns[i]] = pd.Series(r)
		
		subject_dir = 'Data\\Subject_' + str(self.subject)
		if not os.path.exists(subject_dir):
			os.mkdir(subject_dir) 
		subject_df.to_excel(subject_dir + '\\data.xlsx')
		return subject_df
			