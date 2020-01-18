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

from Data import SubjectData
from DCT import DctTask, TaskData
from OpeningMenu import Menu

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
	
	def create_feedback_canvas(self):
		'''creates the template background of the feedback object'''
		
		self.exp.create_frame(MAIN_FRAME)
		self.exp.create_label(FEEDBACK_LABEL, MAIN_FRAME)
		feedback_label_ref = self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL]
		
		self.feedback_canvas = self.exp.tk.Canvas(feedback_label_ref, width=self.width, height=self.height, bg="Black", highlightbackground="black")
		
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
		self.range_of_feedback = range(self.length_of_feedback)
		
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
	def __init__(self, menu, data_manager, subject_data, phase=None, n_blocks=None):
		super(AfactTaskData, self).__init__(menu, data_manager, subject_data, phase=phase, n_blocks=n_blocks)
		
		self.neutral_running_mean = [] #  holds last 4 neutral RT's, updated throughout the experiment
		self.last_trial_bias = None # holding running mean of n last neutrals, to be changed after every neg trial

	def copmute_running_nutral_mean(self, rt, sentence_instance):
		if sentence_instance.valence == NEUTRAL_SENTENCE:
			self.neutral_running_mean.append(rt)
		if len(self.neutral_running_mean) > 4:
			self.neutral_running_mean = self.neutral_running_mean[1:]
		
	def compute_AFACT_bias_z_score(self, rt, sentence_instance):
		if sentence_instance.valence == NEGATIVE_SENTENCE:
			running_mean = np.mean(self.neutral_running_mean)
			running_std = np.std(self.neutral_running_mean)
			bias = (rt - running_mean)/(1.0*running_std)
			self.last_trial_bias = bias
	
class AfactTask(DctTask):
	def __init__(self, gui, exp, td, flow, afact_gui):
		super(AfactTask, self).__init__(gui, exp, td, flow) # inheriting from the dct class the basic structure and properties
		self.afact_gui = afact_gui
		
	def show_AFACT_frame(self, bias):
		self.gui.after(0, lambda:self.afact_gui.create_feedback(bias))						
		self.gui.after(0, lambda:self.afact_gui.show_feedback_animated(self.gui,bias))
		self.gui.after(10, lambda: self.exp.display_frame(MAIN_FRAME, [FEEDBACK_LABEL]))
		self.gui.after(20, lambda:self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL].pack_forget())
		self.gui.after(30, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text="XXX"))
		self.gui.after(40, lambda:self.exp.display_frame(FRAME_1, [LABEL_1]))
		
	def _continue(self): 
		''' overridded from the parent dct task'''
		x = 0
		if self.td.catch_trials_and_non_catch[self.td.current_trial-1] == 0: # checks if this trial is catch
			#ipdb.set_trace()
			last_sentence = self.td.trials_types_by_phase[self.td.current_trial-1].trial_sent_ref.find_sentence_by_trial(self.td.current_trial-2)
			self.td.copmute_running_nutral_mean(self.td.last_RT, last_sentence) 
			self.td.compute_AFACT_bias_z_score(self.td.last_RT, last_sentence)
			last_sent_valence = last_sentence.valence
			if last_sent_valence == NEGATIVE_SENTENCE:
				bias = self.td.last_trial_bias
				self.gui.after(200, lambda:self.show_AFACT_frame(bias))
				x+=60
	
		self.gui.after(100+x, lambda:super(AfactTask, self)._continue())
		## trial flow control:
		#if self.td.current_sentence.is_practice:
		#	self._give_feedback(self.key_pressed)		
		#	self.gui.after(200+x, self._trial) # TOMER - PAY ATTENTION TO THIS TIME HERE
		#elif self.td.current_trial == self.td.change_block_trial and not self.block_changed:
		#	self.gui.after(200+x, self.change_block_frame) # TOMER - PAY ATTENTION TO THIS TIME HERE
		#elif self.td.catch_trials_and_non_catch[self.td.current_trial] != 0: # checks if this trial is catch
		#	self.gui.after(200+x, self.catch_trial) # intiate catch trial
		#	
		#else:
		#	self.gui.after(200+x, self._trial) # TOMER - PAY ATTENTION TO THIS TIME HERE

bias = 2.5

def main():
	
	def change_feedback(event):
		global bias
		if event.keysym == "Right":
			bias+=0.05
		elif event.keysym == "Left":
			bias-=0.05
		afact_gui.create_feedback(bias)
	
	from ExGui import Experiment
	from processing.TasksAudioDataManager import MainAudioProcessor
	from processing.wav_lengh import AudioProcessor
	from Data import SubjectData
	from ExpFlow import Flow
	
	PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
	PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
	SUBJECT = 'subject'
	GROUP = 'group'
	GENDER = 'gender'
	AUDIOPATH = r'Subjects'
	
	ap = AudioProcessor(PRE_PROCESSED_AUDIO_DF, PROCESSED_AUDIO_DF)
	exp = Experiment()
	gui = exp.gui
	sd = SubjectData()
	flow = Flow()
	
	data_manager = MainAudioProcessor(
										phases_names=[
														AFACT_PHASE, 
														'Post'
														], 
										
										n_trials_by_phase={
															AFACT_PHASE: 20,
															'Post': 40
															}, 
										
										n_practice_trials=1,
										n_start_neutral_trials=4,
										) #  phases_names=None, n_trials_by_phase=None, n_practice_trials=None):
	
	menu = Menu(exp, gui, flow, ap, AUDIOPATH, data_manager) # controls menu gui and imput fields
	menu.menu_data[SUBJECT] = 1 
	menu.menu_data[GROUP] = 1 
	menu.menu_data[GENDER] = 1
	
	
	# lab
	menu.updated_audio_path  = r"C:\Users\user\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	# mine
	menu.updated_audio_path  = r"C:\Users\HP\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	
	
	menu.ap.process_audio(menu.updated_audio_path) # process this subject audio files
	data_manager.__late_init__(menu)
	
	
	atd = AfactTaskData(menu, data_manager, sd, phase=AFACT_PHASE, n_blocks=2)
	atd.event_timed_init()
	afact_gui = AfactGui(gui, exp)
	afact_gui.create_feedback_canvas()
	
	afact_task = AfactTask(gui, exp, atd, flow, afact_gui)
	#gui.bind("<Right>", change_feedback)	
	#gui.bind("<Left>", change_feedback)	
	afact_task.start_task()
	
	#gui.state('zoomed')
	exp.run()
	
if __name__ == '__main__':
	main()