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
BLOCK_CHANGE_WAIT_TIME = 3000
CATCH_TRIAL_PERCENT = 0.125
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
		if self.td.current_sentence.is_practice:
			self._give_feedback(self.key_pressed)		
			self.gui.after(200, self._trial) # TOMER - PAY ATTENTION TO THIS TIMR
		elif self.td.current_trial == self.td.change_block_trial and not self.block_changed:
			self.change_block_frame()
		elif self.td.catch_trials_and_non_catch[self.td.current_trial] != 0: # checks if this trial is catch
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
		if self.td.catch_trials_and_non_catch[self.td.current_trial] == "c": # check if correct
			self.stimulus_live_text = CATCH_SENTENCEE_QUESTION + "\n"  +  self.td.find_sentence_instance(self.td.current_trial-2).text
		else:
			past_sentence = random.randint(0, self.td.current_trial-2) # -1 to ommit the possibility of taking current sentence
			self.stimulus_live_text = CATCH_SENTENCEE_QUESTION + "\n"  + self.td.trials_types_by_phase(past_sentence).text		
	# ask about last sentence 	
		self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
		self.gui.after(500,self._bind_keyboard)
	# ask math?
	
	def _trial(self): # type controls for practice or acttual
		if self.td.current_trial == self.td.change_block_trial:
			self.exp.hide_frame(CHANGE_BLOCK_FRAME)
			self.exp.display_frame(FRAME_1, [LABEL_1])
		
		if self.td.catch_trials_and_non_catch[self.td.current_trial-1] == "c":
			self.td.record_trial(self.shown_num, self.key_pressed, is_catch_trial=True, correct=True)
			self.td.current_trial-=1 # after recording last catch - insures next trial is tuned to the correct trial
		elif self.td.catch_trials_and_non_catch[self.td.current_trial-1] == "w":
			self.td.record_trial(self.shown_num, self.key_pressed, is_catch_trial=True, correct=False)
			self.td.current_trial-=1
		else:
			self.td.record_trial(self.shown_num, self.key_pressed)  # raising trial counter by 1
		

		self.stimulus_live_text = DCT_STIMULI # reconfiguring fixation stimulus
		self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text))
		
		if self.td.current_trial <= self.td.total_ammount_of_trials:
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
	def __init__(self, menu, data_manager, subject_data, phase=None, n_blocks=None):
		
		# user data
		self.menu = menu # contains gender, subject subject's path and group
		self.phase=phase # base-line \ training \ post trainig \ mab \ dichotic
		self.data_manager = data_manager # All tasks data manager
		self.sd = subject_data
		if n_blocks == None:
			self.n_blocks = 1
		else:
			self.n_blocks = n_blocks
		
		
		# RT live data
		self.t0 = 0 # first time point - digit shown
		self.t1 = 0 # second time point - response taken
		self.last_RT = 0

		# trial block trackeeping
		self.current_trial = 0 # first trial starts with a record - so it is intializes current_trial to 1
		self.current_block = 1
		
		# selection of trials to insert catch trials
		self.catch_trials = []
		self.correct_catch_trials = [] # filled in function _create_catch_trials_list
		
		## add here classfication of this list to correct and incorrect response
		
		# current sentence track keeping
		self.current_sentence = None # continan current Sentence instance
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
		self.sentences 					= self.data_manager.sentences_by_phase[self.phase] # sentences by phase after shuffeling, and multplying ammount of sentences accordind to desired ammount of trials by phase
		self.neutral_sentences 			= self.data_manager.neu_sentences_by_phase[self.phase] # A dictionary that holds unique neutral sentences of each phase, number of phases is predetermined by console.py user.
		self.negatives_sentences 		= self.data_manager.neg_sentences_by_phase[self.phase] # the same but negative contain all neutral sentences
		self.catch_trials_and_non_catch = self.data_manager.catch_and_non_catch_trials_list_by_phase[self.phase] # contains 0, "c" or "w" - means no cathc, correct catch, wrong ctach
		
		self.trials_pointers_by_phase 				= self.data_manager.trials_pointers_by_phase[self.phase] 
		self.trials_types_by_phase 					= self.data_manager.trials_types_by_phase[self.phase]
		self.sentences_instances_by_type_by_phase 	= self.data_manager.sentences_instances_by_type_by_phase[self.phase]
		
		self.ammount_of_experimental_trials = len(self.trials_types_by_phase) - self.data_manager.n_practice_trials # excluding practice trials
		self.total_ammount_of_trials =  len(self.trials_types_by_phase) # including practice
		
		# sd is a subject data instance
		self.sd.add_menu_data(self.menu.menu_data[SUBJECT], self.menu.menu_data[GROUP], self.menu.menu_data[GENDER])
		self.change_block_trial = None # To be defined in defin_block_change_trial
		self.define_block_change_trial()
		
		self.updata_current_sentence() # current sentence is set to the first practice trial
	
	def define_block_change_trial(self):
		if self.n_blocks > 1:
			self.change_block_trial = int(1.0*self.total_ammount_of_trials/self.n_blocks)
		else:
			self.change_block_trial
	
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
				
				#print self.last_RT, self.current_trial-1, ' is_catch_trial = ', is_catch_trial, 'correct_catch=', correct,  'was_correct_digit=', was_correct, 'shown- ', num_shown_type, 'typed-', answer_type ## FOR INFO WHILE EDITING ONLY
				print self.current_trial-1, ' is_catch_trial = ', is_catch_trial, ' correct_catch=', correct,  ' was_correct_digit=', was_correct, 'shown- ', num_shown_type, 'typed-', answer_type ## FOR INFO WHILE EDITING ONLY
				self.updata_current_sentence()
				
			elif is_catch_trial:	# last trial was catch
				self.catch_trials_and_non_catch[self.current_trial-1] = 0
				## COMPUTE RIGHT AND WRONG ACCORDING TO THE CATCH
				if correct:
					was_correct = RESPONSE_LABELS_ON_CATCH_TRIALS[key_pressed] == CORRECT_SENTENCE
				elif not correct:
					was_correct = RESPONSE_LABELS_ON_CATCH_TRIALS[key_pressed] == NOT_CORRECT_SENTENCE
				
				## printing trial data and classification:
				#print self.last_RT, self.current_trial-1, ' is_catch_trial = ', is_catch_trial, 'correct_catch=', correct, 'typed_accordingly? ',  was_correct ## FOR INFO WHILE EDITING ONLY
				print self.current_trial-1, ' is_catch_trial = ', is_catch_trial, 'correct_catch=', correct
			
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
	
	def find_sentence_instance(self, trial):
		# this function builds on equal ntr-neg trials types.
		# otherwise, see my solution in its AfacTaskData class
		trial_type = self.trials_types_by_phase[trial]
		pointer = self.trials_pointers_by_phase[trial_type][trial]
		sent = self.sentences_instances_by_type_by_phase[trial_type][pointer]
		
		return sent
		# to access a Sentence --> current_trial => trial_type => trial_pinter => sentences_by_phase
	
	def updata_current_sentence(self):
		if self.current_trial <= self.total_ammount_of_trials:
			''' Task is still running'''
			self.current_sentence = self.find_sentence_instance(self.current_trial - 1)
			self.current_sentence_path = self.sentence_inittial_path + self.current_sentence.file_path
		
		else:		
			''' Task is over'''
			print "End - on update"
			# raise flag of completion
			# get data frame from sd