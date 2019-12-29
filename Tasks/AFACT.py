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
from DCT import DctTask

## sentences directories and files names
#SENTENCE_NAME_COL = 'sentence_name'
#SUBJECT = 'subject'
#GROUP = 'group'
#GENDER = 'gender'
#
## gui properties
#BACKGROUND = "black"
#FOREGROUND = "white"
#CATCH_SENTENCEE_QUESTION = u":האם המשפט האחרון ששמעת היה"
#DCT_STIMULI_FONT = "david 50 bold"
#DCT_STIMULI = u'XXX'
#FIXATION_TIME = 100 																			########### CHANGE WHENR OPERATING TO 1000 ###########
#FEEDBACK_COLOR_DURATAION = 300
#ONE_MILISCOND = 1000
#MILISECONDS_BEFORE_END = 500
#RIGHT ='r'
#LEFT = 'l'
#CORRECT = "green"
#WRONG = "red"
#FRAME_1 = "first"
#LABEL_1 = "label_1"
#CHANGE_BLOCK_FRAME = 'change_block_frame'
#BUTTON_LABEL = 'button_label'
#
## task properties
#EVEN= 'even'
#ODD = 'odd'
#CORRECT_SENTENCE = 1
#NOT_CORRECT_SENTENCE = 0
#RESPONSE_LABELS = {RIGHT : EVEN, LEFT: ODD} 	# should be changed at some point???
#RESPONSE_LABELS_ON_CATCH_TRIALS = {RIGHT : CORRECT_SENTENCE, LEFT: NOT_CORRECT_SENTENCE} 	# should be changed at some point???
#MIN_DIGIT = 1
#MAX_DIGIT = 8
#AMMOUNT_OF_PRACTICE = 3 # ATTEND TO ITS CREATION
#TRIALS = 20 + AMMOUNT_OF_PRACTICE # ensures all 40 sentences are available at experimental level
#BLOCKS = 2
#CHANGE_BLOCK_TRIAL = int((TRIALS - AMMOUNT_OF_PRACTICE)/BLOCKS) + AMMOUNT_OF_PRACTICE
#BLOCK_CHANGE_WAIT_TIME = 3000
#CATCH_TRIAL_PERCENT = 0.25
#PROPORTION_OF_CORRECT_CATCH = 0.5
#NUM_OF_INTIAL_NEUTRAL_REAL_TRIALS = 4
#
## Afact specific constants
MAIN_FRAME = 'afact_frame'
FEEDBACK_LABEL = 'feedback_label'


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
		
		self.feedback_canvas = self.exp.tk.Canvas(feedback_label_ref, width=self.width, height=self.height)
		
		tick_area = self.height*0.8333333333333334
		self.top_space = int((self.height - tick_area)/2)
		bottom_space = tick_area + self.top_space

		self.tick_space = int(tick_area/self.ammount_of_ticks)
		tick_middle = int(self.height/2) # inorder ti nake it 0 to 100
		self.x_middle = int(self.width/2.0)
		
		
		#self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
		#                text="Click the bubbles that are multiples of two.")
		
		
		self.feedback_canvas.create_rectangle(self.x_middle-50, tick_middle, self.x_middle+50, self.height-self.tick_space, fill="")
		
		self.feedback_canvas.create_text(self.x_middle,self.top_space-20,fill="darkblue",font="Thaoma 14 bold",text=u"הטיה גבוה")
		self.feedback_canvas.create_text(self.x_middle,bottom_space+20,fill="darkblue",font="Thaoma 14 bold",text=u"ללא הטיה")
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
		print color
	
	def show_feedback_animated(self, gui, bias_z_score):
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
			
		
class AfactTask(DctTask):
	def __init__(self, gui, exp, td, flow):
		super().__init__(gui, exp, td, flow) # inheriting from the dct class the basic structure and properties
		
		self.n_lst_neutrals = 4 # defines the number of last n trials to compute running mean
		self.last_n_trials_RTs = [] # holds last 4 neutral RT's
		self.running_nutral_mean = None # holding running mean of n last neutrals 
	
	def copmute_running_nutral_mean(self, rt, sentence_instance):
		pass
		
	def compute_AFACT_bias(self):
		pass
	
	def show_AFACT_frame(self):
		pass
		
	def _continue(self): 
	
		self.copmute_running_nutral_mean(self.td.last_RT, self.td.current_sentence)
	
	
		''' overridded from the parent dct task'''
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

bias = 2.5
def main():
	
	
	def change_feedback(event):
		print event
		global bias
		if event.keysym == "Right":
			bias+=0.05
		elif event.keysym == "Left":
			bias-=0.05
		afact_gui.create_feedback(bias)
	
	
	from ExGui import Experiment
	
	exp = Experiment()
	gui = exp.gui
	
	afact_gui = AfactGui(gui, exp)
	afact_gui.create_feedback_canvas()
	#afact_gui.create_feedback(2.8)						# Normal presentation
	afact_gui.show_feedback_animated(gui,2.5)			# Animated presentation
	
	gui.bind("<Right>", change_feedback)	
	gui.bind("<Left>", change_feedback)	
	
	exp.display_frame(MAIN_FRAME, [FEEDBACK_LABEL])
	#gui.state('zoomed')
	exp.run()
	
if __name__ == '__main__':
	main()
	
	
	
	
	
# def create_feedback_canvas(self):
		# '''creates the template background of the feedback object'''
		
		# self.exp.create_frame(MAIN_FRAME)
		# self.exp.create_label(FEEDBACK_LABEL, MAIN_FRAME)
		# feedback_label_ref = self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL]
		
		# self.feedback_canvas = self.exp.tk.Canvas(feedback_label_ref, width=self.width, height=self.height)
		
		# tick_area = self.height*0.8333333333333334
		# top_space = int((self.height - tick_area)/2)
		# bottom_space = tick_area + top_space

		# tick_space = int(tick_area/self.ammount_of_ticks)
		# tick_middle = int(self.height/2) # inorder ti nake it 0 to 100
		# all_ticks = range(self.ammount_of_ticks) + [self.ammount_of_ticks] # including zero and max
		
		# for i,t in enumerate(all_ticks):
			# tick = (t*tick_space) + top_space
			# tick_text = int((self.ammount_of_ticks**2)/2) - i*self.ammount_of_ticks 
			# tick_text = str(tick)
			
			# self.feedback_canvas.create_line(35, tick, 42, tick)
			# self.feedback_canvas.create_text(20,tick,  text=tick_text, font="David 14") 
			# print tick
		
		# self.feedback_canvas.create_line(42,top_space, 42, bottom_space)
		
		
		# self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
        #               text="Click the bubbles that are multiples of two.")
		
		
		# self.feedback_canvas.create_rectangle(68, tick_middle, 168, self.height-tick_space, fill="#ff0000")
		# self.feedback_canvas.pack()