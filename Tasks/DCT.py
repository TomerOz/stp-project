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
import params

#moved to params
# # sentences directories and files names
# SENTENCE_NAME_COL = 'sentence_name'
# SUBJECT = 'subject'
# GROUP = 'group'
# GENDER = 'gender'

# # To Params:
# FIXATION_TIME = 100 																			########### CHANGE WHENR OPERATING TO 1000 ###########
# PRACTICE_FEEDBACK_DURATAION = 300
# ONE_SECOND = 1000
# MILISECONDS_BEFORE_END = 500
# MIN_DIGIT = 1
# MAX_DIGIT = 8
# BLOCK_CHANGE_WAIT_TIME = 3000
# CATCH_TRIAL_RESPONSE_DELAY = 500
# DCT_STIMULI = u'XXX'
# CATCH_SENTENCEE_QUESTION = u":האם המשפט האחרון ששמעת היה"
# DCT_STIMULI_FONT = "david 50 bold"
# RIGHT ='r'
# LEFT = 'l'
# RIGHT_RESPONSE_KEY = "<Right>"
# LEFT_RESPONSE_KEY = "<Left>"

# # gui properties
# BACKGROUND = "black"
# FOREGROUND = "white"
# CORRECT = "green"
# WRONG = "red"
# FRAME_1 = "first"
# LABEL_1 = "label_1"
# CHANGE_BLOCK_FRAME = 'change_block_frame'
# BUTTON_LABEL = 'button_label'

# # task properties
# EVEN= 'even'
# ODD = 'odd'
# CORRECT_SENTENCE = 1
# NOT_CORRECT_SENTENCE = 0
# RESPONSE_LABELS = {RIGHT : EVEN, LEFT: ODD} 	# should be changed at some point???
# RESPONSE_LABELS_ON_CATCH_TRIALS = {RIGHT : CORRECT_SENTENCE, LEFT: NOT_CORRECT_SENTENCE} 	# should be changed at some point???

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
	
	def _getresponse(self, eff=None, key=None):
		self.td.t1 = time.time()													## END OF TIME RECORD
		self.td.record_time()		
		self.key_pressed = key
		
		# unbinding keyboard - to not allow overriding sentences
		self.gui.unbind(RIGHT_RESPONSE_KEY)
		self.gui.unbind(LEFT_RESPONSE_KEY)
		self.td.record_trial(self.shown_num, self.key_pressed)

		# Practice feedback decision
		if self.td.current_sentence.is_practice:
			self._give_feedback(self.key_pressed)		
			self.gui.after(PRACTICE_FEEDBACK_DURATAION, self._continue) # TOMER - PAY ATTENTION TO THIS TIME
		else:
			self._continue()
		
	def _continue(self):
		self.td.current_trial += 1 # raising trial by 1 
		self.td.updata_current_sentence() # updatind sentence - loading everything nedded

		### TOMER-OMER - if changing block is not nessecary, shut down this if
		if self.td.current_trial_type_intance.is_change_block_trial:
			self.change_block_frame()
		elif self.td.current_trial_type_intance.is_instructions:
			self.flow.next()
		elif self.td.current_trial_type_intance.is_catch: # checks if this trial is catch
			self.catch_trial() # intiate catch trial
		else:
			self._trial() # continues to next trial	
							
	def _give_feedback(self, key):
		num_type = self.td._classify_type_of_num(self.shown_num)
		# if correct
		if RESPONSE_LABELS[key] == num_type:
			#self.gui.after(0, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = CORRECT))
			#self.gui.after(PRACTICE_FEEDBACK_DURATAION, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = BACKGROUND))  ### color feedback
			self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text= "Correct"))
			self.gui.after(PRACTICE_FEEDBACK_DURATAION, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text)) # text feedback
		#if wrong
		else:
			#self.gui.after(0, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = WRONG))
			#self.gui.after(PRACTICE_FEEDBACK_DURATAION, lambda:self.exp.ALL_FRAMES[FRAME_1].config(bg = BACKGROUND))
			self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text = "Wrong"))
			self.gui.after(PRACTICE_FEEDBACK_DURATAION, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
				
	def _bind_keyboard(self):
		self.gui.bind(RIGHT_RESPONSE_KEY, lambda eff: self._getresponse(eff, key=RIGHT))
		self.gui.bind(LEFT_RESPONSE_KEY, lambda eff: self._getresponse(eff,key=LEFT))
		
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
		self.stimulus_live_text = CATCH_SENTENCEE_QUESTION + "\n"  +  self.td.current_sentence.text
		self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
		self.gui.after(CATCH_TRIAL_RESPONSE_DELAY,self._bind_keyboard)
		
	def _trial(self):
		'''This function is being called after response to last trial took place.
				First, it records last trial,
				Second, it start the next trial'''

		self.stimulus_live_text = DCT_STIMULI # reconfiguring fixation stimulus
		self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
		
		# Checking if experiment ended:
		if self.td.current_trial < self.td.total_ammount_of_trials:
			''' Task is still running'''
			self.gui.after(FIXATION_TIME, self._start_audio)
		else:		
			''' Task is over'''
			self.gui.unbind(RIGHT_RESPONSE_KEY)
			self.gui.unbind(LEFT_RESPONSE_KEY)
			print "End - on _tria()"
			# get data frame from sd
			self.td.sd.create_data_frame()
			# raise flag of completion
			self.flow.next()
	
	def destroy_change_block_frame_and_continue(self):
		self.exp.hide_frame(CHANGE_BLOCK_FRAME)
		self.exp.display_frame(FRAME_1, [LABEL_1])
		self._continue()
		
	def change_block_frame(self):
		''' To be cancelled in Omer
		Check if i need it to AFACT'''
		
		print "Block changed"
		self.block_changed = True
		self.td.current_block = 2 # updating block number
		block_change_text = u'השלמת את החצי הראשון של המטלה'
		self.exp.create_frame(
								CHANGE_BLOCK_FRAME, 
								full_screen=True,
								background_color=BACKGROUND
								)
		self.exp.create_label(LABEL_1, CHANGE_BLOCK_FRAME, label_text=block_change_text, label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=DCT_STIMULI_FONT, label_justify="center")
		self.exp.create_label(BUTTON_LABEL, CHANGE_BLOCK_FRAME, label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=DCT_STIMULI_FONT, label_justify="center")
		self.exp.create_button(CHANGE_BLOCK_FRAME, BUTTON_LABEL, 'next', self.destroy_change_block_frame_and_continue)
		self.exp.display_frame(CHANGE_BLOCK_FRAME, [LABEL_1, BUTTON_LABEL])
		self.exp.LABELS_BY_FRAMES[CHANGE_BLOCK_FRAME][BUTTON_LABEL].pack_forget()
		self.gui.after(BLOCK_CHANGE_WAIT_TIME, self.exp.LABELS_BY_FRAMES[CHANGE_BLOCK_FRAME][BUTTON_LABEL].pack)
	
	def start_task(self, user_event=None):
		
		if self.td.current_trial == -1:
			self.td.event_timed_init() # user dependet initment of the dct data class
			self._create_task_label()
			self.exp.display_frame(FRAME_1, [LABEL_1])
			
			# count down to experiment task
			t1 = 0
			# COUNTDOWN OPTION
			#k = ONE_SECOND
			#self.gui.after(t1, lambda:self._count_down(num=3))
			#self.gui.after(k, lambda:self._count_down(num=2))
			#self.gui.after(2*k, lambda:self._count_down(num=1))
			#self.gui.after(3*k, self._continue) # experiment was started
			self.gui.after(t1, self._continue) # experiment was started
		
		else:
			self.exp.display_frame(FRAME_1, [LABEL_1])
			t1 = 0
			# COUNTDOWN OPTION
			#k = ONE_SECOND
			#self.gui.after(t1, lambda:self._count_down(num=3))
			#self.gui.after(k, lambda:self._count_down(num=2))
			#self.gui.after(2*k, lambda:self._count_down(num=1))
			#self.gui.after(3*k, self._continue) # experiment was started
			self.gui.after(t1, self._continue) # experiment was started
				
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
		self.current_trial = -1 # task starts by raising this variable by 1 --> assures it starts on Zero
		self.current_block = 1
		
		# selection of trials to insert catch trials
		self.catch_trials = []
		self.correct_catch_trials = [] # filled in function _create_catch_trials_list
		
		## add here classfication of this list to correct and incorrect response
		
		# current sentence track keeping
		self.current_trial_type_intance = None # continan current TrialType instace
		self.current_sentence = None # continan current Sentence instance
		self.current_sentence_path = None # contain path of current sentence audio file
			
	def event_timed_init(self):
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
		self.sentences 					= self.data_manager.sentences_by_phase[self.phase] # sentences by phase after shuffeling, and multplying ammount of sentences accordind to desired ammount of trials by phase
		self.neutral_sentences 			= self.data_manager.neu_sentences_by_phase[self.phase] # A dictionary that holds unique neutral sentences of each phase, number of phases is predetermined by console.py user.
		self.negatives_sentences 		= self.data_manager.neg_sentences_by_phase[self.phase] # the same but negative contain all neutral sentences
		self.catch_trials_and_non_catch = self.data_manager.catch_and_non_catch_trials_list_by_phase[self.phase] # contains 0, "c" or "w" - means no cathc, correct catch, wrong ctach
		
		self.trials_types_by_phase 					= self.data_manager.trials_types_by_phase[self.phase]
		self.sentences_instances_by_type_by_phase 	= self.data_manager.sentences_instances_by_type_by_phase[self.phase]
		
		self.ammount_of_experimental_trials = len(self.trials_types_by_phase) - self.data_manager.n_practice_trials # excluding practice trials
		self.total_ammount_of_trials =  len(self.trials_types_by_phase) # including practice
		self.change_block_trial = self.data_manager.change_block_trials_by_phase[self.phase]
		# sd is a subject data instance
		self.sd.add_menu_data(self.menu.menu_data[SUBJECT], self.menu.menu_data[GROUP], self.menu.menu_data[GENDER])
		
	def _classify_type_of_num(self, num):
		if num % 2 == 0:
			return EVEN
		else:
			return ODD
				
	def start_time_record(self):
		''' This function is called from the show digit function. 
			It ensures time of record happens with digit presentation, 
			as in getting into the *gui.after* que'''
		self.t0 = time.time() 
	
	def record_time(self):
		self.last_RT = self.t1 - self.t0 # if now we are on trial 11 tahn last_RT belongs to trial 10

	def record_trial(self, num_shown, key_pressed):
		num_shown_type = None # because I want to pass it any way to the data collection
	
		if self.current_trial_type_intance.is_normal_trial: # on regular and practice trials			
			# Checking the subject Digit Classification answer:
			num_shown_type = self._classify_type_of_num(num_shown)
			answer_type = RESPONSE_LABELS[key_pressed]   #what did the subject answer based on --> #RESPONSE_LABELS = {RIGHT : 'even', LEFT: 'odd'} 	# should be changed at some point
			if answer_type == num_shown_type:
				was_correct = True
			else:
				was_correct = False
			
		elif self.current_trial_type_intance.is_catch:	# on catch trials
			## COMPUTE RIGHT AND WRONG ACCORDING TO THE CATCH
			if self.current_trial_type_intance.catch_type: # when true; its correct catch sentence
				was_correct = RESPONSE_LABELS_ON_CATCH_TRIALS[key_pressed] == CORRECT_SENTENCE
			elif not self.current_trial_type_intance.catch_type: # when false; its wrong catch sentence
				was_correct = RESPONSE_LABELS_ON_CATCH_TRIALS[key_pressed] == NOT_CORRECT_SENTENCE
			
					
		
		# saving key press in order to pass into Data package
		self.num_shown_type = num_shown_type
		self.is_catch_trial = self.current_trial_type_intance.is_catch
		self.correct = self.current_trial_type_intance.catch_type
		self.last_trial_classification = was_correct
		self.last_key_pressed = key_pressed 
		self.is_normal_trial = self.current_trial_type_intance.is_normal_trial
		
		# saving data 
		self.sd.push_data_packge(self) 	
	
	def get_next_sentence_instance(self, trial_type):
		# returnning the relevant sentence instance
		sent = trial_type.get_current_sentence()
		trial_type.next()
		
		print "#--------------#"
		print trial_type
		print trial_type.index
		print sent
		print "Current Trial: ", self.current_trial
		print "Change Block Trial is on: ", self.change_block_trial
		print "Total ammount of Trials is : ", self.total_ammount_of_trials
		
		print "------END--------"
		
		return sent
		
	def find_sentence_instance(self, trial):
		trial_type = self.trials_types_by_phase[trial]
		return trial_type.get_current_sentence()
	
	def updata_current_sentence(self):
		print self.total_ammount_of_trials
		if self.current_trial < self.total_ammount_of_trials: # Task is still running
			trial_type = self.trials_types_by_phase[self.current_trial]
			# saving in TaskData object a refferece to the current TrialType instance
			self.current_trial_type_intance = trial_type
			self.current_sentence = self.get_next_sentence_instance(trial_type)
			
			if self.current_trial_type_intance.is_normal_trial:	
				self.current_sentence_path = self.sentence_inittial_path + self.current_sentence.file_path
			else:
				self.current_sentence_path = None
		
		else:		
			''' Task is over'''
			print "End - on update"
			# raise flag of completion
			# get data frame from sd