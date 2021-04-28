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
import numpy as np

from .DCT import DctTask, TaskData
from .params import *

## Afact specific constants
MAIN_FRAME = 'afact_frame'
FEEDBACK_LABEL = 'feedback_label'
NEGATIVE_SENTENCE = 'neg' 			# According to audio df excel file
NEUTRAL_SENTENCE = 'ntr'			# According to audio df excel file
AFACT_PHASE = "afact_phase"
FRAME_1 = "first"
LABEL_1 = "label_1"
ALTERNATIVE_TASK_FRAME = "alternative_task_frame"
ALTERNATIVE_TASK_LABEL = "alternative_task_label"


class AfactGui(object):
	
	def __init__(self, gui, exp, width=500, height=600, max_bias_z_score=None):
		self.gui = gui
		self.exp = exp
		self.width = width
		self.height = height
		self.feedback_canvas = None # Will be later created
		self.ammount_of_ticks = 10
		if max_bias_z_score == None:
			self.max_bias_z_score = 3.0
		else:
			self.max_bias_z_score = max_bias_z_score
		
		self.feedback_scale_pic = r'Tasks\AFACTStimuliPictures\FeedbackScale_2.png'
		self.feedback_arrow_pic = r'Tasks\AFACTStimuliPictures\FeedbackArrow.png'
				
		self.scale_resize_factor = 1.8
		self.arrow_resize_factor = 0.8
		
		self.scale_top_tick = 23*self.scale_resize_factor # in px, extracted from microspft "paint" and referrs to this file -> feedback_scale_pic
		self.scale_bottom_tick = 252*self.scale_resize_factor # in px
		
		self.scale_y_location = 0
		self.length_of_feedback = self.scale_bottom_tick - self.scale_top_tick
		
		self.create_feedback_canvas_orginal()
		
		self.alternative_task_canvas_width = 400
		self.alternative_task_canvas_hight = 150
	
	def create_alternative_task_canvas(self):
		self.exp.create_frame(ALTERNATIVE_TASK_FRAME)
		self.exp.create_label(ALTERNATIVE_TASK_LABEL, ALTERNATIVE_TASK_FRAME)
		label_ref = self.exp.LABELS_BY_FRAMES[ALTERNATIVE_TASK_FRAME][ALTERNATIVE_TASK_LABEL]
		
		self.alternative_task_canvas = self.exp.tk_refference.Canvas(label_ref, 
								width=self.alternative_task_canvas_width, 
								height=self.alternative_task_canvas_hight, 
								bg="black", highlightbackground="black")
		self.alternative_task_canvas.create_rectangle(0,0,40,40, fill="white")
		self.alternative_task_canvas.pack(expand=self.exp.tk_refference.YES, fill=self.exp.tk_refference.BOTH)
	
	def create_n_shapes(self, n):
		self.alternative_task_canvas.delete("all")
		width = 40
		height = 40
		space = 10
		#start = round((self.alternative_task_canvas_width - ((n*(width+space))-space))/2)
		#y_start = self.alternative_task_canvas_hight/2 - height/2
		#for n_shapes in range(n):
		#	self.alternative_task_canvas.create_rectangle(start+n_shapes*(width+space),y_start,start+n_shapes*(width+space)+width,height+y_start, fill="white")
		
		n_in_row = 3
		start = round((self.alternative_task_canvas_width - ((n_in_row*(width+space))-space))/2)
		y_start_row_2 = self.alternative_task_canvas_hight/2 - height/2
		y_start_row_1 = y_start_row_2 - height - space
		y_start_row_3 = y_start_row_2 + height + space
		colors = ["white"]*9
		for i in random.sample(list(range(9)), n):
			colors[i]="black"
		for n_shapes in range(n_in_row):
			self.alternative_task_canvas.create_rectangle(start+n_shapes*(width+space),y_start_row_1,start+n_shapes*(width+space)+width,height+y_start_row_1, fill=colors[n_shapes], outline='white')
		for n_shapes in range(n_in_row):
			self.alternative_task_canvas.create_rectangle(start+n_shapes*(width+space),y_start_row_2,start+n_shapes*(width+space)+width,height+y_start_row_2, fill=colors[n_shapes+3], outline='white')
		for n_shapes in range(n_in_row):
			self.alternative_task_canvas.create_rectangle(start+n_shapes*(width+space),y_start_row_3,start+n_shapes*(width+space)+width,height+y_start_row_3, fill=colors[n_shapes+6], outline='white')
		
		
	def create_feedback_canvas_orginal(self):

		self.exp.create_frame(MAIN_FRAME)
		self.exp.create_label(FEEDBACK_LABEL, MAIN_FRAME)
		feedback_label_ref = self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL]
		
		
		self.feedback_canvas = self.exp.tk_refference.Canvas(feedback_label_ref, width=self.width, height=self.height, bg="Black", highlightbackground="black")
		self.y_middle = self.height/2 # inorder ti nake it 0 to 100
		self.x_middle = self.width/2.0
		
		# load the .gif image file
		self.feesback_scale = Image.open(self.feedback_scale_pic)
		self.feesback_scale = self.feesback_scale.resize(
														(int(self.feesback_scale.width*self.scale_resize_factor),
														int(self.feesback_scale.height*self.scale_resize_factor)), 
														Image.ANTIALIAS)
		self.feesback_scale = ImageTk.PhotoImage(self.feesback_scale)
		
		
		# put gif image on canvas
		# pic's upper left corner (NW) on the canvas is at x=50 y=10
		scale_height = self.feesback_scale.height()
		scale_width = self.feesback_scale.width()
		scale_half_width =  scale_width/2.0
		scale_half_hight =  scale_height/2.0
		nw_scale_anchor_x = self.x_middle - scale_half_width 
		self.scale_y_location = self.y_middle-scale_half_hight
		self.feedback_canvas.create_image(nw_scale_anchor_x, self.scale_y_location, image=self.feesback_scale, anchor=self.exp.tk_refference.NW)
		
		self.feedback_arrow = Image.open(self.feedback_arrow_pic)
		self.feedback_arrow = self.feedback_arrow.resize(
														(int(self.feedback_arrow.width*self.arrow_resize_factor),
														int(self.feedback_arrow.height*self.arrow_resize_factor)),
														Image.ANTIALIAS)
		self.feedback_arrow = ImageTk.PhotoImage(self.feedback_arrow)
		feedback_arrow_height = self.feedback_arrow.height()
		feedback_arrow_width = self.feedback_arrow.width()
		
		self.arrow_y = self.scale_y_location + self.scale_top_tick - feedback_arrow_height/2.0 # equvalent to no bias at all
		self.arrow_x = scale_width+nw_scale_anchor_x
		self.feedback_canvas.create_image(self.arrow_x, self.arrow_y, image=self.feedback_arrow, anchor=self.exp.tk_refference.NW, tags='FeedbackArrow')

		self.feedback_canvas.pack(expand=self.exp.tk_refference.YES, fill=self.exp.tk_refference.BOTH)
	
	def create_feedback_original(self, bias_z_score):
		
		gui = self.gui
		if bias_z_score <=0:
			bias_z_score = 0
		
		relative_bias = bias_z_score/self.max_bias_z_score
		
		if relative_bias >= 1.0:
			relative_bias = 1.0
			
		y_feedback = relative_bias*self.length_of_feedback
		self.feedback_canvas.delete("FeedbackArrow")
		self.feedback_canvas.create_image(self.arrow_x, self.arrow_y+y_feedback, image=self.feedback_arrow, anchor=self.exp.tk_refference.NW, tags="FeedbackArrow")
			
	def create_feedback_canvas(self):
		'''creates the template background of the feedback object'''
		
		self.exp.create_frame(MAIN_FRAME)
		self.exp.create_label(FEEDBACK_LABEL, MAIN_FRAME)
		feedback_label_ref = self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL]
		
		self.feedback_canvas = self.exp.tk_refference.Canvas(feedback_label_ref, width=self.width, height=self.height, bg="Black", highlightbackground="black")
		
		tick_area = self.height*0.8333333333333334
		self.top_space = int((self.height - tick_area)/2)
		bottom_space = tick_area + self.top_space

		self.tick_space = int(tick_area/self.ammount_of_ticks)
		tick_middle = int(self.height/2) # inorder ti nake it 0 to 100
		self.x_middle = int(self.width/2.0)
		
		
		#self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
		#                text="Click the bubbles that are multiples of two.")
		
		
		self.feedback_canvas.create_rectangle(self.x_middle-50, tick_middle, self.x_middle+50, self.height-self.tick_space, fill="")
		
		self.feedback_canvas.create_text(self.x_middle,self.top_space-20,fill="lightblue",font="Thaoma 14 bold",text=u"הטיה גבוה")
		self.feedback_canvas.create_text(self.x_middle,bottom_space+20,fill="lightblue",font="Thaoma 14 bold",text=u"ללא הטיה")
		self.length_of_feedback = self.height - 2*(self.tick_space)
		self.range_of_feedback = list(range(self.length_of_feedback))
		
		self.feedback_canvas.pack()
				
	def create_feedback(self, bias_z_score):
		relative_bias = bias_z_score/self.max_bias_z_score
		if relative_bias >= 1.0:
			relative_bias = 1.0
			
		elif relative_bias < 0.0:
			relative_bias = 0.0
			
		y_feedback = int(relative_bias*self.length_of_feedback)
		self.range_of_feedback
		r_feedback_color = hex(int(relative_bias*255))
		r_feedback_color = r_feedback_color[-2:]
		g_feedback_color = hex(255-int(relative_bias*255))
		g_feedback_color = g_feedback_color[-2:]
		
		if r_feedback_color[0] == "x":
			r_feedback_color = "00"
			
		if g_feedback_color[0] == "x":
			g_feedback_color = "00"
		
		color = "#" + r_feedback_color + g_feedback_color + "00"
		self.feedback_canvas.coords(1, self.x_middle-50, self.height-y_feedback-self.top_space, self.x_middle+50, self.height-self.tick_space)
		self.feedback_canvas.itemconfig(1, fill=color)
	
	def show_feedback_animated(self, gui, bias_z_score):
		if bias_z_score <=0:
			bias_z_score = 1
		step = 0.2
		self.bias_z_score = bias_z_score
		self.range_of_biases_until_bias =  np.arange(0,bias_z_score+step, step)
		self.current_i_of_bias = 0
		def for_animation():
			self.current_i_of_bias +=1
			gui.after(3, lambda: self.create_feedback(self.range_of_biases_until_bias[self.current_i_of_bias]))
			if self.current_i_of_bias+1 != len(self.range_of_biases_until_bias):
				gui.after(20,for_animation)
		for_animation()
					
class AfactTaskData(TaskData):
	def __init__(self, menu, data_manager, subject_data, phase=None):
		super(AfactTaskData, self).__init__(menu, data_manager, subject_data, phase=phase)
		
		self.neutral_running_mean = [] #  holds last 4 neutral RT's, updated throughout the experiment
		self.last_trial_bias = None # holding running mean of n last neutrals, to be changed after every neg trial

	def set_classify_num_function(self, afact_alternative):
		if afact_alternative != "original":
			if afact_alternative == "shapes":
				self._classify_type_of_num = self._classify_type_of_num_shapes
			elif afact_alternative == "words":
				self._classify_type_of_num = self._classify_type_of_num_words
		else:
			self._classify_type_of_num = super()._classify_type_of_num
	
	def copmute_running_nutral_mean(self, rt, sentence_instance, current_trial_type_intance):
		if current_trial_type_intance.is_normal_trial: # Avoids; feedbacks, catches, change blocks 
			if sentence_instance.valence == NEUTRAL_SENTENCE:
				self.neutral_running_mean.append(rt)
			if len(self.neutral_running_mean) > 4:
				self.neutral_running_mean = self.neutral_running_mean[1:]
		
	def compute_AFACT_bias_z_score(self, rt, sentence_instance, current_trial_type_intance):
		if current_trial_type_intance.is_normal_trial:
			if sentence_instance.valence == NEGATIVE_SENTENCE:
				running_mean = np.mean(self.neutral_running_mean)
				running_std = np.std(self.neutral_running_mean)
				bias = (rt - running_mean)/(1.0*running_std)
				self.last_trial_bias = bias
				
	def _classify_type_of_num_shapes(self, num):
		if num > 4:
			return GREATER_X
		else:
			return SMALLER_X
	
	def _classify_type_of_num_words(self, word_object):
		if word_object.type == ALIVE:
			return ALIVE
		else:
			return STILL	
			
class AfactTask(DctTask):
	def __init__(self, gui, exp, td, flow, 
				response_labels=None, afact_alternative="original", 
				words_objects=None):
		
		self.afact_alternative = afact_alternative
		self.words_objects = words_objects
		
		if self.afact_alternative != "original":
			if self.afact_alternative == "shapes":
				response_labels = RESPONSE_LABELS_AFACT_ALTERNATIVE_1 # sets this and task data response_labels
				self.possible_nums = [3,5]
				self.digit_func = self._digit_func_shapes
			elif self.afact_alternative == "words":
				self.digit_func = self._digit_func_words
				ipdb.set_trace()
				response_labels = RESPONSE_LABELS_AFACT_ALTERNATIVE_2 # sets this and task data response_labels
		else:
			self.digit_func = super().show_digit
		
		self.show_digit = self.digit_func
		super(AfactTask, self).__init__(gui, exp, td, flow, response_labels=response_labels) # inheriting from the dct class the basic structure and properties
		self.td.set_classify_num_function(self.afact_alternative)
		self.afact_gui = AfactGui(gui, exp)
		self.stimulus_live_text = "+"
		
		
	def show_AFACT_frame(self, bias):
		#self.gui.after(0, lambda:self.afact_gui.create_feedback(bias))						
		#self.gui.after(0, lambda:self.afact_gui.show_feedback_animated(self.gui,bias))
		self.gui.after(0, lambda:self.afact_gui.create_feedback_original(bias))
		self.gui.after(0, lambda: self.exp.display_frame(MAIN_FRAME, [FEEDBACK_LABEL]))
		self.gui.after(AFACT_FEEDBACK_TIME, lambda:self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL].pack_forget())
		self.gui.after(AFACT_FEEDBACK_TIME, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text="+"))
		self.gui.after(AFACT_FEEDBACK_TIME, lambda:self.exp.hide_frame(MAIN_FRAME))
		self.gui.after(AFACT_BLACK_SCREEN_POST_FEEDBACK_TIME, lambda:self.exp.display_frame(FRAME_1, [LABEL_1]))
		self.gui.after(AFACT_BLACK_SCREEN_POST_FEEDBACK_TIME, self._continue)
	
	def start_task(self, user_event=None):
		'''Overritten from DctTask'''
		super(AfactTask, self).start_task(user_event)
		if self.afact_alternative == "shapes":
			self.afact_gui.create_alternative_task_canvas()
		
	def _digit_func_shapes(self):
		i_sampled = random.randint(0,len(self.possible_nums)-1)						########   PREFERABLEY THIS WILL BE TAKEN FROM A PRE EXISTING + PRE READ LIST OF NUMBERS  ##########
		self.shown_num = self.possible_nums[i_sampled]
		self.afact_gui.create_n_shapes(self.shown_num)
		self.exp.display_frame(ALTERNATIVE_TASK_FRAME,[ALTERNATIVE_TASK_LABEL])
	
	def _digit_func_words(self):
		i_sampled = random.randint(0,len(self.words_objects)-1)
		self.shown_word = self.words_objects[i_sampled]
		self.stimulus_live_text = u'' + self.shown_word.word
		self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text)
		self.shown_num = self.shown_word
		
		
	def _continue(self): 
		''' overridded from the parent dct task'''
		if self.td.current_trial > -1:# ignores first trial
			self.td.copmute_running_nutral_mean(self.td.last_RT, self.td.current_sentence, self.td.current_trial_type_intance) 
			self.td.compute_AFACT_bias_z_score(self.td.last_RT, self.td.current_sentence, self.td.current_trial_type_intance)
		
		self.td.current_trial += 1 # raising trial by 1 
		self.td.updata_current_sentence() # updatind sentence - loading everything nedded
		
		self.exp.display_frame(FRAME_1,[LABEL_1])

		# trial flow control:
		if self.td.current_trial_type_intance.is_change_block_trial:
			self.change_block_frame()
		elif self.td.current_trial_type_intance.is_instructions:
			self.flow.next()
		elif self.td.current_trial_type_intance.is_catch: # checks if this trial is catch
			self.catch_trial() # intiate catch trial
		elif self.td.current_trial_type_intance.is_afact_feedback:
			bias = self.td.last_trial_bias
			self.show_AFACT_frame(bias)
		else:
			self._trial() # continues to next trial	

bias = 2.5

def main():
	
	def change_feedback(event):
		global bias
		if event.keysym == "Right":
			bias+=0.05
		elif event.keysym == "Left":
			bias-=0.05
		afact_gui.create_feedback(bias)
	
	
	from processing.TasksAudioDataManager import MainAudioProcessor
	from processing.wav_lengh import AudioProcessor
	from Data import SubjectData
	from ExpFlow import Flow
	from ExGuiTempAfact import Experiment
	from OpeningMenu import Menu

		
	ap = AudioProcessor(PRE_PROCESSED_AUDIO_DF, PROCESSED_AUDIO_DF) # processing audio files data
	exp = Experiment() # A class instance of experiments buildind
	gui  = exp.EXPERIMENT_GUI # the gui object the above mentioned class
	flow = Flow() # A class instance that controls the experiment flow
	sd = SubjectData()	# 
	
	
	phases_names = [
						DIGIT_PRE,
						DIGIT_POST,           
						AFACT_PHASE,
						MAB_PHASE,
						DICHOTIC_PHASE,
					]
	phases_relations = {
							"Digit_before_and_AFACT": [DIGIT_PRE, AFACT_PHASE],
							"MAB_and_AFACT": [MAB_PHASE, AFACT_PHASE],
							"MAB_and_Digit_after": [MAB_PHASE, DIGIT_POST],
							"Dichotic_and_AFACT": [DICHOTIC_PHASE, AFACT_PHASE],
							}
							
	dichotic_phases = [DICHOTIC_PHASE]
	phases_without_catch_trials = [] + dichotic_phases + [MAB_PHASE, AFACT_PHASE]
	n_trials_by_phase = {
															DIGIT_PRE: 			20, # Each n of trials trepresent only one type of valence
															DIGIT_POST:			20,
															AFACT_PHASE:		80, 
															MAB_PHASE: 			30,
															DICHOTIC_PHASE: 	80, # 	Unrelevant because it is beeing set in the DichoticDataManager 
																					# procedure of building blocks and chuncks - Thus, it is a direct 
																					# function of n of blocks, n of chunks and n trials per chunk
															}


	#####################################################################################################################
	
	# GENERAL DATA MANAGER:
	data_manager = MainAudioProcessor(
										phases_names=phases_names,
										n_trials_by_phase=n_trials_by_phase, 
										n_practice_trials=1, #N_PRACTICE_TRIALS,
										phases_without_catch_trials = phases_without_catch_trials,
										dichotic_phases = dichotic_phases,
										phases_relations = phases_relations,
										n_block_per_phase = {AFACT_PHASE : 2},
										n_start_neutral_trials=4,
										# 		define --> n_block_per_phase = {phase_name : n_of_blocks}
										# 		in order to control ammount of blocks for a specific phase
										)
	
	
	

	# MENU:
	menu = Menu(exp, gui, flow, ap, AUDIOPATH, data_manager) # controls menu gui and imput fields
	menu.menu_data[SUBJECT] = 1 
	menu.menu_data[GROUP] = 1 
	menu.menu_data[GENDER] = 1
	
	
	# lab
	#menu.updated_audio_path  = r"C:\Users\user\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	# mine
	menu.updated_audio_path  = r"C:\Users\HP\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	
	
	menu.ap.process_audio(menu.updated_audio_path) # process this subject audio files
	data_manager.__late_init__(menu)
	
	# AFACT:
	atd = AfactTaskData(menu, data_manager, sd, phase=AFACT_PHASE)
	afact_task = AfactTask(gui, exp, atd, flow)
	
	#gui.bind("<Right>", change_feedback)	
	#gui.bind("<Left>", change_feedback)	
	afact_task.start_task()
	
	#gui.state('zoomed')
	exp.run()
'''	RESPONSE_LABELS_ON_CATCH_TRIALS = {RIGHT : CORRECT_SENTENCE, LEFT: NOT_CORRECT_SENTENCE} 	# should be changed at some point??? '''
if __name__ == '__main__':
	main()