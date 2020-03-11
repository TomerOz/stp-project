#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

BACKGROUND = "black"
FOREGROUND = "white"


class Instructions(object):
	def __init__(self, gui, exp, flow, imagepath):
		self.current_pic = 0
		self.exp = exp
		self.gui = gui
		self.flow = flow
		self.imagepath = imagepath
		self.instruction_pics = os.listdir(self.imagepath)
		
	def start_instrunctions(self):
		self.current_pic = 0 # for reset
		self.gui.bind("<space>", self.next_pic)
		self.gui.bind("<space>", self.next_pic)
		self.exp.create_frame("instructions_f", 
				full_screen=True,
				background_color=BACKGROUND)
				
		img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
		self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
		
		self.exp.display_frame("instructions_f", ["instructions_l"])
	
	def show_message(self, text):
		self.exp.LABELS_BY_FRAMES["instructions_f"]["instructions_l"].destroy()	
		self.exp.create_label("instructions_l", "instructions_f", label_text=text)
		self.exp.display_frame("instructions_f", ["instructions_l"])
	
	def get_task_continue_function(self, continue_function):
		self.continue_function = continue_function
		
	def destroy_frame_after_delay(self, gui_event=None):
		self.exp.LABELS_BY_FRAMES["instructions_f"]["instructions_l"].destroy()	
		self.gui.unbind("<space>")
		self.continue_function()

	def present_simple_picture_frame(self, delay_time=None, message_text=None):
		self.exp.create_frame("instructions_f", 
				full_screen=True,
				background_color=BACKGROUND)
				
		img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
		self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
		
		self.gui.after(0, lambda: self.exp.display_frame("instructions_f", ["instructions_l"]))
		self.gui.after(delay_time, lambda: self.show_message(message_text))
		self.gui.after(delay_time, lambda: self.gui.bind("<space>", self.destroy_frame_after_delay))
		
	
	
	def next_pic(self, eff):
		self.current_pic+=1
		if self.current_pic < len(self.instruction_pics):
			img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
			self.exp.LABELS_BY_FRAMES["instructions_f"]["instructions_l"].destroy()
			self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
			self.exp.display_frame("instructions_f", ["instructions_l"])
		else:
			self.gui.unbind("<space>")
			self.exp.hide_frame("instructions_f")
			self.flow.next()