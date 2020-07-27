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

class AfactGui(object):
	
	def __init__(self, gui, exp, width=200, height=400, max_bias_z_score=None):
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
		
		#self.create_feedback_canvas()
		self.create_feedback_canvas_orginal()
	
	def create_feedback_canvas_orginal(self):
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
		
		# load the .gif image file
		self.feesback_scale = self.exp.tk_refference.PhotoImage(file=r'Tasks\AFACTStimuliPictures\FeedbackScale.png')
		# put gif image on canvas
		# pic's upper left corner (NW) on the canvas is at x=50 y=10
		self.feedback_canvas.create_image(0, 0, image=self.feesback_scale, anchor=self.exp.tk_refference.NW)
		
		self.gif1 = self.exp.tk_refference.PhotoImage(file=r'Tasks\AFACTStimuliPictures\FeedbackArrow.png')
		self.feedback_canvas.create_image(10, 10, image=self.gif1, anchor=self.exp.tk_refference.NW, tags='FeedbackArrow')
		# pack the canvas into a frame/form
		ipdb.set_trace()
		# configure images
		# understad coordinates
		# center stimuli
		self.feedback_canvas.pack(expand=self.exp.tk_refference.YES, fill=self.exp.tk_refference.BOTH)
		
	
		
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
	
	def create_feedback_original(self, gui, bias_z_score):
		self.feedback_canvas.pack_forget()
		self.length_of_feedback = 40
		if bias_z_score <=0:
			bias_z_score = 1
		
		relative_bias = bias_z_score/self.max_bias_z_score
		if relative_bias >= 1.0:
			relative_bias = 1.0
			
		elif relative_bias < 0.0:
			relative_bias = 0.0	
		y_feedback = int(relative_bias*self.length_of_feedback)
		self.feedback_canvas.delete("FeedbackArrow")
		self.feedback_canvas.create_image(20, random.randint(0,100), image=self.gif1, anchor=self.exp.tk_refference.NW, tags="FeedbackArrow")
		#self.feedback_canvas.create_image(0, 0, image=self.feesback_scale, anchor=self.exp.tk_refference.NW)
		# pack the canvas into a frame/form
		#self.feedback_canvas.pack(expand=self.exp.tk_refference.YES, fill=self.exp.tk_refference.BOTH)
		self.feedback_canvas.pack()
	
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
	
class AfactTask(DctTask):
	def __init__(self, gui, exp, td, flow):
		super(AfactTask, self).__init__(gui, exp, td, flow) # inheriting from the dct class the basic structure and properties
		self.afact_gui = AfactGui(gui, exp)
		
	def show_AFACT_frame(self, bias):
		#self.gui.after(0, lambda:self.afact_gui.create_feedback(bias))						
		#self.gui.after(0, lambda:self.afact_gui.show_feedback_animated(self.gui,bias))
		self.gui.after(0, lambda:self.afact_gui.create_feedback_original(self.gui,bias))
		self.gui.after(0, lambda: self.exp.display_frame(MAIN_FRAME, [FEEDBACK_LABEL]))
		self.gui.after(3100, lambda:self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL].pack_forget())
		self.gui.after(3100, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text="XXX"))
		self.gui.after(3100, lambda:self.exp.hide_frame(MAIN_FRAME))
		self.gui.after(4500, lambda:self.exp.display_frame(FRAME_1, [LABEL_1]))
		self.gui.after(4500, self._continue)
		
	def _continue(self): 
		''' overridded from the parent dct task'''
	
		if self.td.current_trial > -1:# ignores first trial
			self.td.copmute_running_nutral_mean(self.td.last_RT, self.td.current_sentence, self.td.current_trial_type_intance) 
			self.td.compute_AFACT_bias_z_score(self.td.last_RT, self.td.current_sentence, self.td.current_trial_type_intance)
		
		self.td.current_trial += 1 # raising trial by 1 
		self.td.updata_current_sentence() # updatind sentence - loading everything nedded
		# trial flow control:
		
		if self.td.current_trial_type_intance.is_change_block_trial:
			self.change_block_frame()
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