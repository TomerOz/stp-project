#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipdb
import time
import random
import os
from playsound import playsound
from PIL import Image, ImageTk
g
from ExGui import Experiment
from Tasks.instructions import Instructions
from Tasks.DCT import DctTask, TaskData
from Tasks.OpeningMenu import Menu
from Tasks.processing.wav_lengh import AudioProcessor
from Tasks.processing.TasksAudioDataManager import MainAudioProcessor
from Tasks.Data import SubjectData
from Tasks.ExpFlow import Flow
g

AUDIOPATH = r'Subjects'
IMAGEPATH = r'Instructions_Pictures'

PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
AFACT_PHASE = "afact_phase"


def main():
	ap = AudioProcessor(PRE_PROCESSED_AUDIO_DF, PROCESSED_AUDIO_DF) # processing audio files data
	exp = Experiment() # A class instance of experiments buildind
	gui  = exp.EXPERIMENT_GUI # the gui object the above mentioned class
	flow = Flow() # A class instance that controls the experiment flow
	sd = SubjectData()	# 
	instructions = Instructions(task, gui, exp, flow, IMAGEPATH)# controls instructions gui and flow
	
	data_manager = MainAudioProcessor(
										phases_names=[AFACT_PHASE, 'Post'], 
										n_trials_by_phase={AFACT_PHASE: 40,'Post':40}, 
										n_practice_trials=4) #  phases_names=None, n_trials_by_phase=None, n_practice_trials=None):
	
	menu = Menu(exp, gui, flow, ap, AUDIOPATH, data_manager) # controls menu gui and imput fields
	td_trainig = TaskData(menu, data_manager, sd, phase='Baseline', n_blocks=2) # A class intance that organizes the data for the DCT task
	td_post_training = TaskData(menu, data_manager, sd, phase='Post') # A class intance that organizes the data for the DCT task
	task = DctTask(gui, exp, td_trainig, flow) # A class intance that runs the DCT task
		
	tasks = [
				lambda: menu.show(),
				lambda: instructions.start_instrunctions(),
				lambda: task.start_task(),
				]
				
	flow.add_tasks(tasks)
	
	gui.bind("<space>", flow.start_exp)
	gui.state('zoomed')
	#exp._full_screen_creator(gui) # for running in a complete full screen
	exp.run()
	
if __name__ == "__main__":
	main()
