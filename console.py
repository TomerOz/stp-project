#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipdb
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
from Tasks.Data import SubjectData
from Tasks.ExpFlow import Flow
from Tasks.processing.DichoticDataManager import DichoticTrialsManager
from Tasks.dichotic import DichoticOneBack, DichoticTaskData

from Tasks.params import *

# AUDIOPATH = r'Subjects'
# IMAGEPATH = r'Instructions_Pictures'
# IMAGEPATH_DICHOTIC_PRACTICE_ONE = r'Instructions_Pictures\Dichotic\DichoticInst1'
# IMAGEPATH_DICHOTIC_PRACTICE_TWO = r'Instructions_Pictures\Dichotic\DichoticInst2'
# IMAGEPATH_DICHOTIC = r'Instructions_Pictures\Dichotic\DichoticInst3'

# IMAGEPATH_DCT_PRACTICE_1 = r'Instructions_Pictures\Digitnew\DigitInstTomerOmer\digit1'
# IMAGEPATH_DCT_PRACTICE_2 = r'Instructions_Pictures\Digitnew\DigitInstTomerOmer\digit2'
# IMAGEPATH_DCT_PRACTICE_3 = r'Instructions_Pictures\Digitnew\DigitInstTomerOmer\digit3'
# IMAGEPATH_DICHOTIC_BREAK = r'Instructions_Pictures\Dichotic\DichoticInst4'
	
# PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
# PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
# AFACT_PHASE = "afact_phase"
# DICHOTIC_PHASE_STR = 'dichotic_phase'

# N_BASELINE_TRIALS = 10
# N_POST_TRIALS = 10
# N_AFACT_TRIALS = 20
# N_DICHOTIC_TRIALS = 20
# N_PRACTICE_TRIALS = 8

def main():
	ap = AudioProcessor(PRE_PROCESSED_AUDIO_DF, PROCESSED_AUDIO_DF) # processing audio files data
	exp = Experiment() # A class instance of experiments buildind
	gui  = exp.EXPERIMENT_GUI # the gui object the above mentioned class
	flow = Flow() # A class instance that controls the experiment flow
	sd = SubjectData()	# 
	instructions = Instructions(gui, exp, flow, IMAGEPATH)# controls instructions gui and flow
	
	
	
	# Has to match to "n_list" in TaksAudioDataManager in _split_senteces_to_phases (line ~151)
	phases_names = [DIGIT_PRE, DIGIT_POST, DICHOTIC_PRE, DICHOTIC_POST]
	
	
	data_manager = MainAudioProcessor(
										phases_names=phases_names,
										n_trials_by_phase={
															DIGIT_PRE: 			80, # 40 neutrals and 40 negtaives
															DIGIT_POST:			80,
															DICHOTIC_PRE:		120, # unrelevant - because the code deletes it 	
															DICHOTIC_POST: 		120,
															}, 
										n_practice_trials=N_PRACTICE_TRIALS,
										phases_without_catch_trials = [DICHOTIC_PRE, DICHOTIC_POST, AFACT_PHASE],
										dichotic_phases = [DICHOTIC_PRE, DICHOTIC_POST],
										#n_block_per_phase = {"Baseline" : 2},
										# define --> n_block_per_phase = {phase_name : n_of_blocks}
										# in order to control ammount of blocks for a specific phase
										)
	
	dichotic_task_gui = DichoticOneBack(gui, exp)
	
	instructions_dct_1 = Instructions(gui, exp, flow, IMAGEPATH_DCT_PRACTICE_1)
	instructions_dct_2 = Instructions(gui, exp, flow, IMAGEPATH_DCT_PRACTICE_2)
	instructions_dct_3 = Instructions(gui, exp, flow, IMAGEPATH_DCT_PRACTICE_3)
		
	instructions_dichotic_1 = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_PRACTICE_ONE)# controls instructions gui and flow
	instructions_dichotic_2 = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_PRACTICE_TWO)# controls instructions gui and flow
	instructions_dichotic_3 = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC)# controls instructions gui and flow
	instructions_dichotic_break = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_BREAK)# controls instructions gui and flow
	instructions_dichotic_end = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_END)# controls instructions gui and flow
	
	
	menu = Menu(exp, gui, flow, ap, AUDIOPATH, data_manager) # controls menu gui and imput fields
	
	# maybe duplicate it for pre and post - AT THE MOMENT ITS ONLY "PRE"
	dichotic_data_manager = DichoticTrialsManager(gui, flow, data_manager, DICHOTIC_PRE)
	dichotic_task_data = DichoticTaskData(exp, flow, dichotic_task_gui, dichotic_data_manager, data_manager, gui, menu, instructions_dichotic_break)
	
	td_trainig = TaskData(menu, data_manager, sd, phase=DIGIT_PRE) # A class intance that organizes the data for the DCT task
	td_post_training = TaskData(menu, data_manager, sd, phase=DIGIT_POST) # A class intance that organizes the data for the DCT task
	dct_training = DctTask(gui, exp, td_trainig, flow) # A class intance that runs the DCT task
	dct_post_training = DctTask(gui, exp, td_post_training, flow) # A class intance that runs the DCT task
	
	instructions_digit_end = Instructions(gui, exp, flow, IMAGEPATH_DIGIT_END)# controls instructions gui and flow
	
	instructions_end_of_experiment = Instructions(gui, exp, flow, IMAGEPATH_END_OF_EXPERIMENT)# controls instructions gui and flow
	
	tasks = [
				lambda: menu.show(),
				lambda: dichotic_data_manager.__late_init__()   ,
				lambda: dichotic_task_data.__late_init__()      ,
				
				#lambda: instructions_dct_1.start_instrunctions(),
				#lambda: dct_training.start_task(),
				#lambda: instructions_dct_2.start_instrunctions(),
				#lambda: dct_training.start_task(),
				#lambda: instructions_dct_3.start_instrunctions(),
				#lambda: dct_training.start_task(),
				#
				#lambda: instructions_end_of_experiment.start_instrunctions(),
				#lambda: instructions_dichotic_end.start_instrunctions(break_time=3000),
				
				#lambda:instructions_dichotic_1.start_instrunctions(),
				#lambda: dichotic_task_data.first_practice(side="Left"),				
				#lambda: dichotic_task_data.first_practice(side="Right"),
				#lambda:instructions_dichotic_2.start_instrunctions(),
				#lambda: dichotic_task_data.second_practice(),
				#lambda:instructions_dichotic_3.start_instrunctions(),
				lambda: dichotic_task_data.start_chunk(),
				lambda: instructions_dichotic_end.start_instrunctions(break_time=3000),
				lambda: instructions_end_of_experiment.start_instrunctions(),
				
				# insert here some silence
			
				
				]
				
	flow.add_tasks(tasks)
	
	gui.bind("<space>", flow.next)
	gui.state('zoomed')
	#exp._full_screen_creator(gui) # for running in a complete full screen
	exp.run()
	
if __name__ == "__main__":
	main()
