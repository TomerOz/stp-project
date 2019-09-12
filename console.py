#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import ipdb
import time
import random
import os
from playsound import playsound
from PIL import Image, ImageTk

from ExGui import Experiment
from Tasks.instructions import Instructions
from Tasks.DCT import DctTask, TaskData
from Tasks.OpeningMenu import Menu
from Tasks.processing.wav_lengh import AudioProcessor
from Tasks.processing.TasksAudioDataManager import MainAudioProcessor

CALLBACK_WAIT_TIME = 500

#AUDIOPATH = r'G:\Shared drives\Amit Bernstein Lab - HIPAA\omertomer\DCT_STP\Subjects'
#IMAGEPATH = r'G:\Shared drives\Amit Bernstein Lab - HIPAA\omertomer\DCT_STP\Instructions_Pictures'

AUDIOPATH = r'Subjects'
IMAGEPATH = r'Instructions_Pictures'

PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task

def main():
	
	class Flow(object):
		def __init__(self, gui):
			self.flag = False # controling the execution of the function to be called
			self.gui = gui
		
		def callback(self, fanc_to_call, *args):
			if self.flag:
				fanc_to_call(*args)
				self.flag = False
			else:
				self.gui.after(CALLBACK_WAIT_TIME, lambda:self.callback(fanc_to_call, *args))
	
		def start_exp(self, eff):	# eff is just the irelevant event passed with the binding
			''' This is the exprimental flow defacto.
					Any new task or unrealted windo should appear here.
					Tomer - consider integrating this class inside ExpGui'''
			
			self.gui.unbind("<Right>")	
			menu.show()
			self.callback(instructions.inst_flow)
			self.callback(task.start_task)

		def second_task(self, event=None):
			self.flag = True
			self.gui.unbind("<Right>")
			self.gui.unbind("<Left>")
			self.callback(instructions2.inst_flow)
			self.callback(task2.start_task)
	
	ap = AudioProcessor(PRE_PROCESSED_AUDIO_DF, PROCESSED_AUDIO_DF)
	exp = Experiment()
	gui  = exp.EXPERIMENT_GUI
	flow = Flow(gui)
	data_manager = MainAudioProcessor()
	menu = Menu(exp, gui, flow, ap, AUDIOPATH, data_manager)
	td_trainig = TaskData(menu, data_manager, phase='training')
	td_post_training = TaskData(menu, data_manager, phase='post')
	task = DctTask(gui, exp, td_trainig, flow)
	instructions = Instructions(task, gui, exp, flow, IMAGEPATH)
	
	task2 = DctTask(gui, exp, td_post_training, flow)
	instructions2 = Instructions(task, gui, exp, flow, IMAGEPATH)
	
	gui.bind("<space>", flow.start_exp)
	gui.state('zoomed')
	#exp._full_screen_creator(gui) # for running in a complete full screen
	exp.run()
	
if __name__ == "__main__":
	main()
