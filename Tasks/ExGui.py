#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
from PIL import Image, ImageTk
import ctypes

class Experiment(object):
	''' this class creates a full functioning experiment building on Tk GUI. 
	it has the abillity to create frames (full_screen),enable navigation between frames, configure frames
	take responses, create csv of responses, create buttons, create messages, and create scales.'''
	
	EXPERIMENT_GUI = tk.Tk() # main window of this experiment
	EXPERIMENT_GUI.configure(background ='black')
	
	ALL_FRAMES = {} # contains all frames to be later packed, unpacked or refference in any other way
	LABELS_BY_FRAMES = {} # shaped as {fame_name: {label_name1 : label_1, ..., labeln_name : labeln}...} 
	ALL_SCALES = {}
	SCALE_VARIABLES = {}
	ALL_ENTRIES = {}
	QUESTIONS_TEXT_LABELS = {}
	#					frame_n : {...}} ## frame name is a string.
	BUTTONS = {}
	CURRENT_FRAME = None # keeps track on currently displayed frame
	
	def __init__(self, font_color="white", background="black"):
		self.gui = type(self).EXPERIMENT_GUI
		self.tk = tk
		user32 = ctypes.windll.user32
		self.screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		self.x = self.screensize[0] #screen width
		self.y = self.screensize[1] #screen height
		self.cx = int(self.screensize[0]*0.5) #screen width center
		self.cy = int(self.screensize[1]*0.5) #screen hight center
	
	def _full_screen_creator(self, tk_object):

		tk_object.overrideredirect(True)
		tk_object.overrideredirect(False)
		tk_object.attributes('-fullscreen',True)
	
	def craete_smart_image_label(
									self,
									label_name,
									frame_name,
									path,
									resize_to=False,
									label_text=None, 
									label_fg='black',
									label_bg='white',
									label_font='david 28 bold',
									label_justify='right',
									blank_label_width=160,
									blank_label_height=10,
									blank_label=False,
									image_label=True,
									label_image=None
								):
		
		''' the same as create label but here u only provide path '''
		
		pic = Image.open(path)
		if resize_to != False:
			pic = pic.resize((resize_to[0], resize_to[1]), Image.ANTIALIAS)
		
		final_pic = ImageTk.PhotoImage(pic)
			
		self.create_label(
					label_name,
					frame_name, 
					label_text, 
					label_fg,
					label_bg,
					label_font,
					label_justify,
					blank_label_width,
					blank_label_height,
					blank_label,
					image_label,
					label_image=final_pic,
					
					)
					
	def create_question(
						self,
						parent_frame,
						parent_label,
						entry_reffernce_name,
						question_text,
						pack_side='left',
						):
		
		entry_label = tk.Label(type(self).LABELS_BY_FRAMES[parent_frame][parent_label])
		entry_local = tk.Entry(entry_label)
		type(self).ALL_ENTRIES[entry_reffernce_name] = entry_local
		
		
		text_label = tk.Label(type(self).LABELS_BY_FRAMES[parent_frame][parent_label], text=question_text)
		type(self).QUESTIONS_TEXT_LABELS[entry_reffernce_name] = text_label
		
		type(self).ALL_ENTRIES[entry_reffernce_name].pack()
		entry_label.pack(side = pack_side)
		type(self).QUESTIONS_TEXT_LABELS[entry_reffernce_name].pack(side = pack_side)
		
	
	def create_entry(
						self,
						entry_name,
						parent,
						pack_style=None,
					):
		
		''' creates and packs an entry in a parent (expected to be a label)'''
		
		local_entry = tk.Entry(parent)	
		type(self).ALL_ENTRIES[entry_name] = local_entry
		type(self).ALL_ENTRIES[entry_name].pack(side = pack_style)
						
	def create_frame(
						
						self, 
						frame_name, 
						parent=None,
						full_screen=True,
						background_color='gray'
				):
	
		''' frame_name should be a string.
		by default width and hight are adjusted to the main window's properties'''
		
		if full_screen == True:
			if parent != None:
				parent = type(self).ALL_FRAMES[parent]
			else:
				parent = type(self).EXPERIMENT_GUI
				
			frame = tk.Frame(parent, width = self.x, height = self.y)
		
		else:
			if parent != None:
				parent = type(self).ALL_FRAMES[parent]
			else:
				parent = type(self).EXPERIMENT_GUI
				
			frame = tk.Frame(parent)
		
		type(self).ALL_FRAMES[frame_name] = frame
		type(self).ALL_FRAMES[frame_name].configure(background = background_color)
		type(self).LABELS_BY_FRAMES[frame_name] = {}
			
	def create_label(
					self, 
					label_name,
					frame_name, 
					label_text=None, 
					label_fg='black',
					label_bg='gray',
					label_font='david 28 bold',
					label_justify='right',
					label_width=None,
					label_height=None,
					blank_label=False,
					image_label=False,
					label_image=None,
					anchor="center"
				):
		
			
		if blank_label == False and image_label == False:
			
			label = tk.Label(
									type(self).ALL_FRAMES[frame_name], 
									text = label_text, 
									fg = label_fg,
									bg = label_bg,
									font = label_font,
									justify = label_justify,
									)
	
			if frame_name in type(self).ALL_FRAMES.keys():
				type(self).LABELS_BY_FRAMES[frame_name][label_name] = label
			else:
				type(self).LABELS_BY_FRAMES[frame_name] = {label_name : label}
		
		elif blank_label == True:
			
			label = tk.Label(
								type(self).ALL_FRAMES[frame_name], 
								bg = label_bg,
								width = blank_label_width,
								height = blank_label_height
						)
	
			if frame_name in type(self).ALL_FRAMES.keys():
				type(self).LABELS_BY_FRAMES[frame_name][label_name] = label
			else:
				type(self).LABELS_BY_FRAMES[frame_name] = {label_name : label}
		
		elif image_label == True:
			label_with_image = tk.Label(type(self).ALL_FRAMES[frame_name], image=label_image, bg = 'gray')
			label_with_image.image = label_image
			if frame_name in type(self).ALL_FRAMES.keys():
				type(self).LABELS_BY_FRAMES[frame_name][label_name] = label_with_image
			else:
				type(self).LABELS_BY_FRAMES[frame_name] = {label_name : label_with_image}
		
	## ALL OBJECTS (e.g. BUTTONS, SCALES, PICTURES, VIDEOS ETC.) ARE PACKED WITHIN LABLES WHICH ARE THEN PACKED WITHIN FRAMES 
	
	def create_scale(
						self,
						frame_name,
						label_name,
						scale_name,
						s_color='blue',
						default_range=(-50,50),
						show_value=False,
						orientation=tk.HORIZONTAL,
						s_length=600,
						initial_score=0
					):
		# creating a variable attached to the scale			
		type(self).SCALE_VARIABLES[scale_name] = tk.IntVar()
		# creating the scale instance
		scale = tk.Scale(
							type(self).LABELS_BY_FRAMES[frame_name][label_name], 
							troughcolor = s_color, 
							from_=default_range[0], to=default_range[1], 
							showvalue =show_value, 
							orient=orientation, 
							length = s_length, 
							variable = type(self).SCALE_VARIABLES[scale_name],
						)
		# keeping a reffernce
		type(self).ALL_SCALES[scale_name] = scale
		# setting initial score
		type(self).ALL_SCALES[scale_name].set(initial_score)
		# packing
		type(self).ALL_SCALES[scale_name].pack()
	
	def create_button(
						self, 
						frame_name,
						label_name,
						button_text, 
						button_command, 
						pack_style=None,
						button_name=None,
						button_width=None,
						button_height=None
					):
		''' frame name is a *string* and specifies the frame in which to pack the button'''
		## all hard coded values should move to a new class which its properties can be changed easiliy ##
		
		button = tk.Button(
							type(self).LABELS_BY_FRAMES[frame_name][label_name], 
							bd = 6, 
							activebackground = "green", 
							relief = "raised", 
							cursor = "cross", 
							font = 'david', 
							bg = "white", 
							text = button_text, 
							fg = "black", 
							command = button_command,
							width = button_width,
							height = button_height
						)
		if button_name!= None:
			type(self).BUTTONS[button_name] = button
		button.pack(side = pack_style)
	
	def display_frame(self, frame_name, labels_order, pack_style=None, use_place=False): 
	# use_place is a dictionary that contains label name as key and a tuple of coordinates x and y)
		for label in labels_order:
			if use_place != False:
				if label in use_place.keys():
					if label in type(self).LABELS_BY_FRAMES[frame_name].keys():
						type(self).LABELS_BY_FRAMES[frame_name][label].place(x = use_place[label][0], y = use_place[label][1], anchor='nw')
					else:
						type(self).ALL_FRAMES[label].place(x = use_place[label][0], y = use_place[label][1], anchor='nw') #this is aimed to deal with frames within frames
				else: 
					if label in type(self).LABELS_BY_FRAMES[frame_name].keys():
						type(self).LABELS_BY_FRAMES[frame_name][label].pack(side=pack_style, expand=1)
					else:
						type(self).ALL_FRAMES[label].pack()
			else:
				if label in type(self).LABELS_BY_FRAMES[frame_name].keys():
					type(self).LABELS_BY_FRAMES[frame_name][label].pack(side=pack_style, expand=1)
				else:
					type(self).ALL_FRAMES[label].pack() #this is aimed to deal with frames within frames
										
		if type(self).CURRENT_FRAME != None:
			self.hide_frame(type(self).CURRENT_FRAME)
		
		type(self).CURRENT_FRAME = frame_name
		type(self).ALL_FRAMES[frame_name].pack(expand =1, fill = tk.BOTH)
	
	def hide_frame(self, frame_name):
		type(self).ALL_FRAMES[frame_name].pack_forget()
	
	def run(self):
		type(self).EXPERIMENT_GUI.mainloop()
		
def main():
	pass

if __name__ == "__main__":
	main()