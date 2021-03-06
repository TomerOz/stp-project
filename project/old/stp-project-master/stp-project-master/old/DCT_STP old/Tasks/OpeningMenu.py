#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Tkinter as tk

BACKGROUND = "black"
FOREGROUND = "white"

gender = 	'gender'
group = 	'group'
subject =	'subject'

class Menu(object):
	def __init__(self, exp, gui, flow, ap, audiopath):
		self.exp = exp
		self.gui = gui
		self.flow = flow
		self.ap = ap
		self.audiopath = audiopath
		self.menu_data = {}
		
		self.create_menu()
		
	def create_menu(self):
		self.exp.create_frame('menu_frame', full_screen=True, background_color=BACKGROUND)
		
		self.exp.create_label('menu_label_1', 'menu_frame', label_bg = BACKGROUND) 
		self.exp.create_label('menu_label_2', 'menu_frame', label_bg = BACKGROUND)
		self.exp.create_label('menu_label_3', 'menu_frame', label_bg = BACKGROUND)
		self.exp.create_label('button_label', 'menu_frame', label_bg = BACKGROUND)
		
		self.exp.create_button('menu_frame', 'button_label', 'Start', self.start)
		
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
		self.exp.display_frame('menu_frame', ['menu_label_1', 'menu_label_2', 'menu_label_3', 'button_label'], use_place = self.places)
		
	def start(self):
		self.menu_data[gender] = type(self.exp).ALL_ENTRIES[gender].get()
		self.menu_data[group] = type(self.exp).ALL_ENTRIES[group].get()
		self.menu_data[subject] = type(self.exp).ALL_ENTRIES[subject].get()
		
		self.updated_audio_path  = self.audiopath + '\\' + 'subject ' + str(self.menu_data[subject])	
		self.ap.process_audio(self.updated_audio_path) # process this subject audio files
		
		self.flow.flag =True
		
