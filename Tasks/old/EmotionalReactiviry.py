#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Build a moduled Gui task, that loops through several rmotions from a list and send it to the subject data manager
	include instructions from pictures.
"""

import ipdb
import time
import random
import os
import pandas as pd
from PIL import Image, ImageTk
#from playsound import playsound
#import winsound

from Data import SubjectData

MAIN_FRAME = "main frame"
EMOTION_LABEL = "emotion_label"
EMOTION_LEVEL_N_FRAME = "emotion_n_{}"
EXTREME_RIGHT_E_LABLE = "extreme_right_e_lable" # the text description of the scale end
EXTREME_LEFT_E_LABLE = "extreme_left_e_lable" # the text description of the scale end
BUTTON_LABEL = "button_label"

class EmotionalReactivityTask(object):
	def __init__(self, er_gui, e_data_task, experimental_phase):
		self.e_data_task = e_data_task
		self.experimental_phase = experimental_phase
		self.emotions = self.e_data_task.keys()
		
		
		random.shuffle(self.emotions)
	
		self.answers = {} # subject, emotion, answer, phase, trial,
		self.current_emotion_trial = 0
		

		self.er_gui = er_gui
		self.er_gui.create_er_template(5, self.next_emotion)
		self.er_gui.create_er_boxes_and_places()
		self.er_gui.create_canvases()
		self.er_gui._bind_to_hover_functions()
		
		l_label_x = self.er_gui.scale_places[EMOTION_LEVEL_N_FRAME.format(str(0))][0] + int(self.er_gui.er_level_box_width/2.0) - self.er_gui.er_space_width
		r_label_x = self.er_gui.scale_places[EMOTION_LEVEL_N_FRAME.format(str(self.er_gui.scale_range-1))][0] + int(self.er_gui.er_level_box_width/2.0) - self.er_gui.er_space_width
		self.e_labels_places = {
								EMOTION_LABEL: (self.er_gui.exp.cx-60, 60),
								EXTREME_RIGHT_E_LABLE : (r_label_x, self.er_gui.exp.cy),
								EXTREME_LEFT_E_LABLE : (l_label_x, self.er_gui.exp.cy),
								BUTTON_LABEL : (self.er_gui.exp.cx-30, int(self.er_gui.exp.y*0.85))
									}

	def next_emotion(self):
		self.current_emotion_trial += 1
		self.probe_emotion()
		for c in self.er_gui.canvases:
			self.er_gui.canvases_states[c] = "no"
			self.er_gui._change_item(c, 0.7, "#207010")
			c.bind("<Enter>", self.er_gui.on_enter)
			c.bind("<Leave>", self.er_gui.on_leave)
		
		self.er_gui.exp.BUTTONS["Next_btn"].config(state="disabled")
		
	def probe_emotion(self):
		ekey = self.emotions[self.current_emotion_trial]
		txt = self.e_data_task[ekey]["text"]
		r = self.e_data_task[ekey]["R"]
		l = self.e_data_task[ekey]["L"]
		self.er_gui.exp.LABELS_BY_FRAMES[MAIN_FRAME][EMOTION_LABEL].config(text = txt)
		self.er_gui.exp.LABELS_BY_FRAMES[MAIN_FRAME][EXTREME_RIGHT_E_LABLE].config(text = r)
		self.er_gui.exp.LABELS_BY_FRAMES[MAIN_FRAME][EXTREME_LEFT_E_LABLE].config(text = l)
		
	def run_task(self):
	
		all_places_dict = {}
		all_places_dict.update(self.er_gui.scale_places)
		all_places_dict.update(self.e_labels_places)
		disp_list = [EMOTION_LABEL, EXTREME_RIGHT_E_LABLE, EXTREME_LEFT_E_LABLE, BUTTON_LABEL] + self.er_gui.scale_places.keys()
		self.er_gui.exp.display_frame(MAIN_FRAME, disp_list, use_place=all_places_dict)
		self.probe_emotion()

class EmotionalReactivityGui(object):
	
	def __init__(self, gui, exp, scale_range):
		self.gui = gui
		self.exp = exp
		self.scale_range = scale_range
		self.scale_places = {}
		self.canvases = [] # holding the emotions canvases
		self.ovals = {}
		self.boxes_heights = 240
		self.canvases_states = {} # canvas object as key - state as value

	def create_er_template(self, scale_range, bt_command):
	
		self.exp.create_frame(MAIN_FRAME)
		self.exp.create_label(EMOTION_LABEL, MAIN_FRAME)
		
		for i in range(scale_range):
			self.exp.create_frame(EMOTION_LEVEL_N_FRAME.format(str(i)), background_color="red") # USING CHILD FRAMES IN ORDER TO CONTROL THEIE WIDHT, not possible with lables
			
		self.exp.create_label(EXTREME_RIGHT_E_LABLE, MAIN_FRAME)
		self.exp.create_label(EXTREME_LEFT_E_LABLE, MAIN_FRAME)
		self.exp.create_label(BUTTON_LABEL, MAIN_FRAME)
		self.exp.create_button(MAIN_FRAME, BUTTON_LABEL, u"המשך", bt_command, button_name="Next_btn")
		self.exp.BUTTONS["Next_btn"].config(state="disabled")

	def create_er_boxes_and_places(self):
		self._compute_scale_places(self.scale_range)
		start = self.er_left_edge + self.er_space_width
		
		for i in range(self.scale_range):
			self.exp.ALL_FRAMES[EMOTION_LEVEL_N_FRAME.format(str(i))].config(width = self.er_level_box_width, height=self.boxes_heights)
			er_box_x = start + i*(self.er_level_box_width+self.er_space_width)
			self.scale_places[EMOTION_LEVEL_N_FRAME.format(str(i))] = (er_box_x,self.exp.cy*1.1)
	
	def create_canvases(self):
		x1=int(self.er_level_box_width*0.3/2.0)
		x2=int(self.er_level_box_width*0.7) + x1
		y1=int(self.boxes_heights*0.3/2.0)
		y2=int(self.boxes_heights*0.7) + x1
		
		for i in range(self.scale_range):
			frame = self.exp.ALL_FRAMES[EMOTION_LEVEL_N_FRAME.format(str(i))]
			canvas = self.exp.tk.Canvas(frame, bg="grey", width = self.er_level_box_width, height=self.boxes_heights, bd=0,  highlightthickness=0)
			self.canvases.append(canvas)
			oval = canvas.create_oval(x1,y1,x2,y2, fill="#207010", outline="")
			self.ovals[canvas] = oval
			canvas.pack(fill="both", expand=1)
	
	def _change_item(self, w, size, color):
		rest = 1.0-size
		x1=int(self.er_level_box_width*rest/2.0)
		x2=int(self.er_level_box_width*size) + x1
		y1=int(self.boxes_heights*rest/2.0)
		y2=int(self.boxes_heights*size) + x1
		
		w.coords(1, x1,y1,x2,y2)
		w.itemconfig(1, fill=color)
	
	
	def on_enter(self, event):
		self._change_item(event.widget, 0.9, "#309020")
		
	def on_click(self, event):
		self.exp.BUTTONS["Next_btn"].config(state="normal")
		self.canvases_states[event.widget] = "yes"
		self._change_item(event.widget, 0.9, "#062006")
		
		event.widget.unbind("<Enter>")
		event.widget.unbind("<Leave>")
		
		for c in self.canvases:
			if c != event.widget:
				self.canvases_states[c] = "no"
				self._change_item(c, 0.7, "#207010")
				c.bind("<Enter>", self.on_enter)
				c.bind("<Leave>", self.on_leave)
			
	def on_leave(self, event):
		self._change_item(event.widget, 0.7, "#207010")
	
	def _bind_to_hover_functions(self):
		for i in self.canvases:
			i.bind("<Enter>", self.on_enter)
			i.bind("<Leave>", self.on_leave)
			i.bind("<Button-1>", self.on_click)
			
	def _compute_scale_places(self, scale_range):
		screen_width = self.exp.x
		scale_area_width = int(screen_width*0.9)
		left_edge = int((screen_width - scale_area_width)/2.0) # the left edge of the right margin
		right_edge = left_edge + scale_area_width # the right edge of thr left margin
		
		space_total_area = int(scale_area_width*0.1)
		spaces_ammount = scale_range + 1
		space_width = int(1.0*space_total_area/spaces_ammount)
		er_level_box_width =  int((scale_area_width-space_total_area)/scale_range) # each level of emotional reactivty box width
		
		self.er_level_box_width = er_level_box_width
		self.er_space_width =     space_width
		self.er_right_edge =      right_edge
		self.er_left_edge =       left_edge 
	
def main():
	
	from ExGui import Experiment
	
	exp = Experiment()
	gui = exp.gui
	
	e_data_task = {
					"Fear": 
						{
						"text": u"פחד גדול",
						"R": u"קטן",
						"L": u"גדול"
						},
					"Anger":
						{
						"text": u"כעס",
						"R": u"אני כאן",
						"L": u"וגם פה"
						}
					}
	
	
	er_gui = EmotionalReactivityGui(gui, exp, 5)
	ert = EmotionalReactivityTask(er_gui, e_data_task, "try")
	ert.run_task()
	
	
	
	gui.state('zoomed')
	exp.run()
	
if __name__ == '__main__':
	main()