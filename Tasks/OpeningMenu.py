#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk

BACKGROUND = "black"
FOREGROUND = "white"

gender = 	'gender'
group = 	'group'
subject =	'subject'

class Menu(object):
	def __init__(self, exp, gui, flow, ap, audiopath, data_manager, dichotic_task_data=None):
		self.exp = exp
		self.gui = gui
		self.flow = flow
		self.ap = ap
		self.audiopath = audiopath
		self.menu_data = {}
		self.data_manager = data_manager
		self.dichotic_task_data = dichotic_task_data
		self.create_menu()
		
	def create_menu(self):
		self.exp.create_frame('menu_frame', full_screen=True, background_color=BACKGROUND)
		
		self.exp.create_label('menu_label_1', 'menu_frame', label_bg = BACKGROUND) 
		self.exp.create_label('menu_label_2', 'menu_frame', label_bg = BACKGROUND)
		self.exp.create_label('menu_label_3', 'menu_frame', label_bg = BACKGROUND)
		self.exp.create_label('button_label', 'menu_frame', label_bg = BACKGROUND)
		
		self.exp.create_button('menu_frame', 'button_label', 'Start', self.start_button_callback)
		
		self.exp.create_question('menu_frame', 'menu_label_1', gender, u'  מגדר ')
		self.exp.create_question('menu_frame', 'menu_label_2', group, u'  קבוצה')
		self.exp.create_question('menu_frame', 'menu_label_3', subject, u'  נבדק')
		
		dy = 30
		self.places = {
		'menu_label_1':(self.exp.cx, self.exp.cy-dy),
		'menu_label_2':(self.exp.cx, self.exp.cy),
		'menu_label_3':(self.exp.cx, self.exp.cy+dy),
		'button_label':(self.exp.cx, self.exp.cy+dy*3),
		}
	def show(self):
		self.gui.unbind("<space>")
		self.exp.display_frame('menu_frame', ['menu_label_1', 'menu_label_2', 'menu_label_3', 'button_label'], use_place = self.places)
		
	def start_button_callback(self):
		self.menu_data[gender] = type(self.exp).ALL_ENTRIES[gender].get()
		self.menu_data[group] = type(self.exp).ALL_ENTRIES[group].get()
		self.menu_data[subject] = type(self.exp).ALL_ENTRIES[subject].get()
		
		self.updated_audio_path  = self.audiopath + '\\' + 'subject ' + str(self.menu_data[subject])	
		
		self.ap.process_audio(self.updated_audio_path) # process this subject audio files
		self.data_manager.__late_init__(self)
		# If dichituc task was given as argument
		if self.dichotic_task_data != None:
			self.dichotic_task_data.dichotic_data_manager.__late_init__()
			self.dichotic_task_data.__late_init__()
		
		self.flow.next()
		
