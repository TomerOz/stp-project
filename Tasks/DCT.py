#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipdb
import time
import random
import os
import pandas as pd
from playsound import playsound
from PIL import Image, ImageTk
import winsound

from Data import SubjectData

# sentences directories and files names
SENTENCE_NAME_COL = 'sentence_name'
SUBJECT = 'subject'
GROUP = 'group'
GENDER = 'gender'

# gui properties
BACKGROUND = "black"
FOREGROUND = "white"
CATCH_SENTENCEE_QUESTION = u":האם המשפט האחרון ששמעת היה"
DCT_STIMULI_FONT = "david 50 bold"
DCT_STIMULI = u'XXX'
FIXATION_TIME = 100 																			########### CHANGE WHENR OPERATING TO 1000 ###########
FEEDBACK_COLOR_DURATAION = 300
ONE_MILISCOND = 1000
MILISECONDS_BEFORE_END = 500
RIGHT ='r'
LEFT = 'l'
CORRECT = "green"
WRONG = "red"
FRAME_1 = "first"
LABEL_1 = "label_1"
CHANGE_BLOCK_FRAME = 'change_block_frame'
BUTTON_LABEL = 'button_label'

# task properties
EVEN= 'even'
ODD = 'odd'
CORRECT_SENTENCE = 1
NOT_CORRECT_SENTENCE = 0
RESPONSE_LABELS = {RIGHT : EVEN, LEFT: ODD} 	# should be changed at some point???
RESPONSE_LABELS_ON_CATCH_TRIALS = {RIGHT : CORRECT_SENTENCE, LEFT: NOT_CORRECT_SENTENCE} 	# should be changed at some point???
MIN_DIGIT = 1
MAX_DIGIT = 8
AMMOUNT_OF_PRACTICE = 3 # ATTEND TO ITS CREATION
TRIALS = 20 + AMMOUNT_OF_PRACTICE # ensures all 40 sentences are available at experimental level
BLOCKS = 2
CHANGE_BLOCK_TRIAL = int((TRIALS - AMMOUNT_OF_PRACTICE)/BLOCKS) + AMMOUNT_OF_PRACTICE
BLOCK_CHANGE_WAIT_TIME = 3000
CATCH_TRIAL_PERCENT = 0.25
PROPORTION_OF_CORRECT_CATCH = 0.5
NUM_OF_INTIAL_NEUTRAL_REAL_TRIALS = 4

class DctTask(object):
	
	def __init__(self, gui, exp, td, flow):
		self.gui = gui
		self.exp = exp
		self.td = td
		self.flow = flow
		self.stimulus_live_text = DCT_STIMULI # to be later updated
		self.shown_num = None # last number on screen
		self.key_pressed = None
		self.block_changed = False # keeps track if lasts block change occured
		
	def _getreponse(self, eff=None, key=None):
		self.td.t1 = time.time()													## END OF TIME RECORD
		self.td.record_time()		
		self.key_pressed = key
		self.td.current_trial += 1 # raising trial by 1 
		
		# unbinding keyboard - to not allow overriding sentences
		self.gui.unbind("<Right>")
		self.gui.unbind("<Left>")
		self._continue()
		
	def _continue(self):
		# trial flow control:
		if self.td.is_practice:
			self._give_feedback(self.key_pressed)		
			self.gui.after(200, self._trial) # TOMER - PAY ATTENTION TO THIS TIMR
		elif self.td.current_trial == CHANGE_BLOCK_TRIAL and not self.block_changed:
			self.change_block_frame()
		elif self.td.current_trial in self.td.catch_trials:
			self.catch_trial() # intiate catch trial
		else:
			self._trial() # continues to next trial			
			
	def _give_feedback(self, key):
		num_type = self.td._classify_type_of_num(self.shown_num)
		# if correct
		if RESPONSE_LABELS[key] == num_type:
			#self.gui.after(0, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = CORRECT))
			#self.gui.after(FEEDBACK_COLOR_DURATAION, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = BACKGROUND))  ### color feedback
			self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text= "ok"))
			self.gui.after(FEEDBACK_COLOR_DURATAION, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text)) # text feedback
		#if wrong
		else:
			#self.gui.after(0, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = WRONG))
			#self.gui.after(FEEDBACK_COLOR_DURATAION, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = BACKGROUND))
			self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text = "not"))
			self.gui.after(FEEDBACK_COLOR_DURATAION, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
				
	def _bind_keyboard(self):
		self.gui.bind("<Right>", lambda eff: self._getreponse(eff, key=RIGHT))
		self.gui.bind("<Left>", lambda eff: self._getreponse(eff,key=LEFT))
		
	def _start_audio(self):
		playsound(self.td.current_sentence_path, block=False) 						# audio is taken every trial from an updating filename 
		
		self.gui.after(self.td.current_sentence.digit_que, self.show_digit)
		self.gui.after(self.td.current_sentence.digit_que, self._bind_keyboard) 	# ensures that binding ocurs with digit
		self.gui.after(self.td.current_sentence.digit_que, self.td.start_time_record)  ## START OF TIME RECORD 	- this format makes it happen before digit delay presentation *self.td.t0 = time.time()*
			
	def show_digit(self):
		self.shown_num = random.randint(MIN_DIGIT,MAX_DIGIT)						########   PREFERABLEY THIS WILL BE TAKEN FROM A PRE EXISTING + PRE READ LIST OF NUMBERS  ##########
		self.stimulus_live_text = 'X' + str(self.shown_num) +'X'
		self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text)
	
	def _create_task_label(self):
		self.exp.create_frame(
								FRAME_1, 
								full_screen=True,
								background_color=BACKGROUND
								)
		self.exp.create_label(LABEL_1, FRAME_1, label_text=DCT_STIMULI, label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=DCT_STIMULI_FONT, label_justify="center")
		
	def _count_down(self, num=None):
		self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=str(num))
	
	def catch_trial(self):
		self.td.record_trial(self.shown_num, self.key_pressed) # records prior regular trial
		if self.td.current_trial in self.td.correct_catch_trials:
			self.stimulus_live_text = CATCH_SENTENCEE_QUESTION + "\n"  +  self.td.sentences[self.td.current_trial-2].text
		else:
			past_sentence = random.randint(0, self.td.current_trial-2) # -1 to ommit the possibility of taking current sentence
			self.stimulus_live_text = CATCH_SENTENCEE_QUESTION + "\n"  + self.td.sentences[past_sentence].text		
	# ask about last sentence 	
		self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
		self.gui.after(500,self._bind_keyboard)
	# ask math?
	
	def _trial(self): # type controls for practice or acttual
		if self.td.current_trial == CHANGE_BLOCK_TRIAL:
			self.exp.hide_frame(CHANGE_BLOCK_FRAME)
			self.exp.display_frame(FRAME_1, [LABEL_1])
		
		if self.td.current_trial-1 in self.td.correct_catch_trials:
			self.td.record_trial(self.shown_num, self.key_pressed, is_catch_trial=True, correct=True)
			self.td.current_trial-=1 # after recording last catch - insures next trial is tuned to th correct trial
		elif self.td.current_trial-1 in self.td.catch_trials:
			self.td.record_trial(self.shown_num, self.key_pressed, is_catch_trial=True, correct=False)
			self.td.current_trial-=1
		else:
			self.td.record_trial(self.shown_num, self.key_pressed)  # raising trial counter by 1
		

		self.stimulus_live_text = DCT_STIMULI # reconfiguring fixation stimulus
		self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
		
		if self.td.current_trial <= TRIALS:
			''' Task is still running'''
			self.gui.after(FIXATION_TIME, self._start_audio)
		else:		
			''' Task is over'''
			print "End - on _tria()"
			# get data frame from sd
			self.td.sd.create_data_frame()
			# raise flag of completion
			self.flow.second_task()
	
	def change_block_frame(self):
		print "Block changed"
		self.block_changed = True
		self.td.current_block = 2 # updating block
		block_change_text = u'השלמת את החצי הראשון של המטלה'
		self.exp.create_frame(
								CHANGE_BLOCK_FRAME, 
								full_screen=True,
								background_color=BACKGROUND
								)
		self.exp.create_label(LABEL_1, CHANGE_BLOCK_FRAME, label_text=block_change_text, label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=DCT_STIMULI_FONT, label_justify="center")
		self.exp.create_label(BUTTON_LABEL, CHANGE_BLOCK_FRAME, label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=DCT_STIMULI_FONT, label_justify="center")
		self.exp.create_button(CHANGE_BLOCK_FRAME, BUTTON_LABEL, 'next', self._continue)
		self.exp.display_frame(CHANGE_BLOCK_FRAME, [LABEL_1, BUTTON_LABEL])
		self.exp.LABELS_BY_FRAMES[CHANGE_BLOCK_FRAME][BUTTON_LABEL].pack_forget()
		self.gui.after(BLOCK_CHANGE_WAIT_TIME, self.exp.LABELS_BY_FRAMES[CHANGE_BLOCK_FRAME][BUTTON_LABEL].pack)
	
	def start_task(self):
		self.td.event_timed_initment() # user dependet initment of the dct data class
		self._create_task_label()
		self.exp.display_frame(FRAME_1, [LABEL_1])
		
		# count down to experiment task
		t1 = 0
		k = ONE_MILISCOND
		self.gui.after(t1, lambda:self._count_down(num=3))
		self.gui.after(k, lambda:self._count_down(num=2))
		self.gui.after(2*k, lambda:self._count_down(num=1))
		self.gui.after(3*k, self._trial) # experiment was started
		
				
class TaskData(object):
	''' the data manager of the dct task'''
	
	def __init__(self, menu, data_manager, subject_data, phase=None):
		
		# user data
		self.menu = menu # contains gender, subject subject's path and group
		self.phase=phase # base-line \ training \ post trainig \ mab \ dichotic
		self.data_manager = data_manager # All tasks data manager
		self.sd = subject_data

		# RT live data
		self.t0 = 0 # first time point - digit shown
		self.t1 = 0 # second time point - response taken
		self.last_RT = 0

		# trial block trackeeping
		self.current_trial = 0 # first trial starts with a record - so it is intializes current_trial to 1
		self.current_block = 1
		self.is_practice = True
		
		# selection of trials to insert catch trials
		self.catch_trials = []
		self.correct_catch_trials = [] # filled in next function
		self._create_catch_trials_list()
		## add here classfication of this list to correct and incorrect response
		
		# current sentence track keeping
		self.current_sentence = None # continan Sentence current instance
		self.current_sentence_path = None # contain path of current sentence audio file
			
	def event_timed_initment(self):
		'''
			This is part of the regular initment process though it is evoked only when 
			other process are finished like getting menu data from user.
			consider other way to incorporate this process.
		'''
		# Getting sentences info from main data manager
		self.audio_path = 			self.data_manager.audio_path
		self.audio_df = 			self.data_manager.audio_df
		self.audio_files_path = 	self.data_manager.audio_files_path
		self.sentence_inittial_path =  self.data_manager.sentence_inittial_path
		self.audio_files_list = 	self.data_manager.audio_files_list
		
		
		# adresss according to instructinos
		self.sentences 					= self.data_manager.sentences # sentences to be used in the current phase - be it pre or post trainig -- updates within program
		self.neutral_sentences 			= self.data_manager.neutral_sentences # contain all neutral sentences
		self.negatives_sentences 		= self.data_manager.negatives_sentences # contain all negative sentences
		self.pre_intervention_sentences = self.data_manager.pre_intervention_sentences
		self.post_intervention_sentences = self.data_manager.post_intervention_sentences
		
		self.training_neutrals 				= self.data_manager.training_neutrals
		self.post_training_neutrals         = self.data_manager.post_training_neutrals
		self.training_negatives             = self.data_manager.training_negatives
		self.post_training_negatives        = self.data_manager.post_training_negatives
		
		self.pre_intervention_sentences     = self.data_manager.pre_intervention_sentences
		self.post_intervention_sentences    = self.data_manager.post_intervention_sentences
		
		
		# sd is a subject data instance
		self.sd.add_menu_data(self.menu.menu_data[SUBJECT], self.menu.menu_data[GROUP], self.menu.menu_data[GENDER])
		
		self.practice_trials = [] # contain sentences of practivce
		self._redefine_sentences_according_to_phase(phase=self.phase)
		self._get_x_practice_trials() # practice trials are dublicated and added
		self.updata_current_sentence() # current sentence is set to the first practice trial
	
	
	def _classify_type_of_num(self, num):
		if num % 2 == 0:
			return EVEN
		else:
			return ODD
			
	def _create_catch_trials_list(self):
		catch_trials_ammount = int(CATCH_TRIAL_PERCENT*TRIALS)
		trials = range(AMMOUNT_OF_PRACTICE+2,TRIALS+1) # + 2 so that first two trials are not catch
		for i in range(catch_trials_ammount):
			num = random.sample(trials, 1)[0]
			trials.remove(num)
			self.catch_trials.append(num)
			if num-1 in trials:
				trials.remove(num-1)
			if num+1 in trials:
				trials.remove(num+1)	
		self.memory_of_catch_trials = [] + self.catch_trials # catch_trials will be changed and this one not.
		
		#creating catch trials of correct types
		self.correct_catch_trials = random.sample(self.catch_trials, int(PROPORTION_OF_CORRECT_CATCH*len(self.catch_trials)))
				
	def start_time_record(self):
		''' This function is called from the show digit function. 
			It ensures time of record happens with digit presentation, 
			as in getting into the *gui.after* que'''
		self.t0 = time.time() 
	
	def record_time(self):
		self.last_RT = self.t1 - self.t0 # if now we are on trial 11 tahn last_RT belongs to trial 10
	
	def record_trial(self, num_shown, key_pressed, is_catch_trial=False, correct=False):
		
		num_shown_type = None # because I want to pass it any way to the data collection
		if key_pressed!=None: # after first trial
			if not is_catch_trial: # on regular and practice trials
				num_shown_type = self._classify_type_of_num(num_shown)
				answer_type = RESPONSE_LABELS[key_pressed]   #what did the subject answer based on --> #RESPONSE_LABELS = {RIGHT : 'even', LEFT: 'odd'} 	# should be changed at some point
				if answer_type == num_shown_type:
					was_correct = True
				else:
					was_correct = False
				
				if self.current_trial > AMMOUNT_OF_PRACTICE:
					self.is_practice = False
				
				print self.last_RT, self.current_trial-1, ' is_catch_trial = ', is_catch_trial, 'correct_catch=', correct,  'was_correct_digit=', was_correct, 'shown- ', num_shown_type, 'typed-', answer_type ## FOR INFO WHILE EDITING ONLY
				self.updata_current_sentence()
				
			elif is_catch_trial:	# last trial was catch
				self.catch_trials.remove(self.current_trial-1)
				## COMPUTE RIGHT AND WRONG ACCORDING TO THE CATCH
				if correct:
					self.correct_catch_trials.remove(self.current_trial-1)
					was_correct = RESPONSE_LABELS_ON_CATCH_TRIALS[key_pressed] == CORRECT_SENTENCE
				elif not correct:
					was_correct = RESPONSE_LABELS_ON_CATCH_TRIALS[key_pressed] == NOT_CORRECT_SENTENCE
				
				## printing trial data and classification:
				print self.last_RT, self.current_trial-1, ' is_catch_trial = ', is_catch_trial, 'correct_catch=', correct, 'typed_accordingly? ',  was_correct ## FOR INFO WHILE EDITING ONLY
			
			# saving key press in order to pass into Data package
			self.num_shown_type = num_shown_type
			self.is_catch_trial = is_catch_trial
			self.correct = correct
			self.last_trial_classification = was_correct
			self.last_key_pressed = key_pressed 
			self.sd.push_data_packge(self) # saving data
		
		else: # on first trial
			self.current_trial += 1
			self.updata_current_sentence()
		
	def _redefine_sentences_according_to_phase(self, phase=None):
		# re definig sentences lists to the current phase -  pre or post training
		# currently sets to trainnig phase
		if phase == 'training':
			self.sentences = self.pre_intervention_sentences
			self.neutral_sentences = self.training_neutrals
			self.negatives_sentences = self.training_negatives 
		elif phase == 'post':
			self.sentences = self.post_intervention_sentences
			self.neutral_sentences = self.post_training_neutrals
			self.negatives_sentences = self.post_training_negatives			
	
	def _get_x_practice_trials(self, neutrals=AMMOUNT_OF_PRACTICE, negatives=0):
		'''
			after sentences were randomized and insured d neutrals to start with
			additional x practice trial are added at the beginig
		'''
		neutral_practice = random.sample(self.neutral_sentences, neutrals)
		negative_practice = random.sample(self.negatives_sentences, negatives)
		
		self.practice_trials = neutral_practice + negative_practice
		random.shuffle(self.practice_trials)
		
		self.sentences = self.practice_trials + self.sentences # inserting practice trials to the beginig of sentences
				
	def updata_current_sentence(self):
		if self.current_trial <= TRIALS:
			''' Task is still running'''
			self.current_sentence = self.sentences[self.current_trial - 1]
			self.current_sentence_path = self.sentence_inittial_path + self.current_sentence.file_path
		
		else:		
			''' Task is over'''
			print "End - on update"
			# raise flag of completion
			# get data frame from sd