#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import ipdb 

BACKGROUND = "black"
FOREGROUND = "white"

gender = 	'gender'
group = 	'group'
subject =	'subject'
session = 'session'

class Menu(object):
	def __init__(self, exp, gui, flow, ap, audiopath, data_manager):
		self.exp = exp
		self.gui = gui
		self.flow = flow
		self.data_manager = data_manager
		self.ap = ap
		self.audiopath = audiopath
		self.menu_data = {}
		self.create_menu()
		
	def create_menu(self):
		self.exp.create_frame('menu_frame', full_screen=True, background_color=BACKGROUND)
		
		self.exp.create_label('menu_label_1', 'menu_frame', label_bg = BACKGROUND) 
		self.exp.create_label('menu_label_2', 'menu_frame', label_bg = BACKGROUND)
		self.exp.create_label('menu_label_3', 'menu_frame', label_bg = BACKGROUND)
		self.exp.create_label('menu_label_4', 'menu_frame', label_bg = BACKGROUND)
		
		
		self.exp.create_question('menu_frame', 'menu_label_1', gender, u'  מגדר ')
		self.exp.create_question('menu_frame', 'menu_label_2', group, u'  קבוצה')
		self.exp.create_question('menu_frame', 'menu_label_3', subject, u'  נבדק')
		self.exp.create_question('menu_frame', 'menu_label_4', session, u'  סשן')
		
		dy = 30
		self.places = {
		'menu_label_1':(self.exp.cx, self.exp.cy-dy),
		'menu_label_2':(self.exp.cx, self.exp.cy),
		'menu_label_3':(self.exp.cx, self.exp.cy+dy),
		'menu_label_4':(self.exp.cx, self.exp.cy+(2*dy)),
		}
	def show(self):
		self.gui.unbind("<space>")
		self.exp.display_frame('menu_frame', ['menu_label_1', 'menu_label_2', 'menu_label_3', 'menu_label_4'], use_place = self.places)
		self.gui.bind("<space>", self.start_space_callback)
		
	def start_space_callback(self, event=None):
		self.menu_data[gender] = type(self.exp).ALL_ENTRIES[gender].get()
		self.menu_data[group] = type(self.exp).ALL_ENTRIES[group].get()
		self.menu_data[subject] = type(self.exp).ALL_ENTRIES[subject].get()
		self.menu_data[session] = type(self.exp).ALL_ENTRIES[session].get()
		
		self.updated_audio_path  = self.audiopath + '\\' + 'subject ' + str(self.menu_data[subject])	
		self.ap.process_audio(self.updated_audio_path) # process this subject audio files
		self.data_manager.__late_init__(self)
		self.gui.unbind("<space>")
		self.exp.hide_cursor()
		self.flow.next()
