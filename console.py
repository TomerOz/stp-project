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
from Tasks.MAB import MABTask, MABTaskData
from Tasks.AFACT import AfactTask, AfactTaskData
from Tasks.BMM import BMMTask, BMMTaskData
from Tasks.OpeningMenu import Menu
from Tasks.processing.wav_lengh import AudioProcessor
from Tasks.processing.TasksAudioDataManager import MainAudioProcessor
from Tasks.Data import SubjectData
from Tasks.ExpFlow import Flow
from Tasks.processing.DichoticDataManager import DichoticTrialsManager
from Tasks.dichotic import DichoticOneBack, DichoticTaskData
from Tasks.bodymap.run_sample import ConsoleBodyMap
from Tasks.processing.AfactWordsAlternative.words_to_list import get_words_objects

from Tasks.params import *

def main():
	ap = AudioProcessor(PRE_PROCESSED_AUDIO_DF, PROCESSED_AUDIO_DF) # processing audio files data
	exp = Experiment() # A class instance of experiments buildind
	gui  = exp.EXPERIMENT_GUI # the gui object the above mentioned class
	flow = Flow() # A class instance that controls the experiment flow
	sd = SubjectData()	# 
	instructions = Instructions(gui, exp, flow, IMAGEPATH)# controls instructions gui and flow
	
	# Tomer:
	# Has to match to "n_list" in TaksAudioDataManager in _split_senteces_to_phases (line ~151)	
	
	phases_names = [
						DIGIT_PRE,
						DIGIT_POST,           
						AFACT_PHASE,
						MAB_PHASE,
						DICHOTIC_PHASE,
					]
	phases_relations = {
							"Digit_before_and_AFACT": [DIGIT_PRE, AFACT_PHASE],
							"MAB_and_AFACT": [MAB_PHASE, AFACT_PHASE],
							"MAB_and_Digit_after": [MAB_PHASE, DIGIT_POST],
							"Dichotic_and_AFACT": [DICHOTIC_PHASE, AFACT_PHASE],
							}
							
	dichotic_phases = [DICHOTIC_PHASE]
	phases_without_catch_trials = [] + dichotic_phases + [MAB_PHASE, AFACT_PHASE]
	n_trials_by_phase = {
															DIGIT_PRE: 			20, # Each n of trials trepresent only one type of valence
															DIGIT_POST:			20,
															AFACT_PHASE:		80, 
															MAB_PHASE: 			30,
															DICHOTIC_PHASE: 	80, # 	Unrelevant because it is beeing set in the DichoticDataManager 
																					# procedure of building blocks and chuncks - Thus, it is a direct 
																					# function of n of blocks, n of chunks and n trials per chunk
															}


	#####################################################################################################################
	
	# GENERAL DATA MANAGER:
	data_manager = MainAudioProcessor(
										phases_names=phases_names,
										n_trials_by_phase=n_trials_by_phase, 
										phases_without_catch_trials = phases_without_catch_trials,
										dichotic_phases = dichotic_phases,
										phases_relations = phases_relations,
										n_block_per_phase = {AFACT_PHASE : 2},
										#####################################################################################################################
										n_practice_trials=N_PRACTICE_TRIALS,
										n_start_neutral_trials=DEFAULT_N_START_NEUTRAL_TRIALS, #### on running = 4, DEFAULT_N_START_NEUTRAL_TRIALS supposed to be 4 ####
										n_afact_practice_trials=N_PRACTICE_TRIALS, #### on running = 8, N_PRACTICE_TRIALS supposed to be 8 ####
										#####################################################################################################################
										
										# 		define --> n_block_per_phase = {phase_name : n_of_blocks}
										# 		in order to control ammount of blocks for a specific phase
										)
	
	
	# INSTUCTIONS:
	instructions_dct_1 = Instructions(gui, exp, flow, IMAGEPATH_DCT_PRACTICE_1)
	instructions_dct_2 = Instructions(gui, exp, flow, IMAGEPATH_DCT_PRACTICE_2)
	instructions_dct_3 = Instructions(gui, exp, flow, IMAGEPATH_DCT_PRACTICE_3)
		
	instructions_dichotic_1 = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_PRACTICE_ONE)# controls instructions gui and flow
	instructions_dichotic_2 = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_PRACTICE_TWO)# controls instructions gui and flow
	instructions_dichotic_3 = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC)# controls instructions gui and flow
	instructions_dichotic_break = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_BREAK)# controls instructions gui and flow
	instructions_dichotic_end = Instructions(gui, exp, flow, IMAGEPATH_DICHOTIC_END)# controls instructions gui and flow
	
	instructions_digit_end = Instructions(gui, exp, flow, IMAGEPATH_DIGIT_END)# controls instructions gui and flow
	instructions_end_of_experiment = Instructions(gui, exp, flow, IMAGEPATH_END_OF_EXPERIMENT)# controls instructions gui and flow
	
	# MENU:
	menu = Menu(exp, gui, flow, ap, AUDIOPATH, data_manager) # controls menu gui and imput fields
	
	# DICHOTIC
	dichotic_task_gui = DichoticOneBack(gui, exp)
	dichotic_data_manager = DichoticTrialsManager(gui, flow, data_manager, menu, DICHOTIC_PHASE, n_blocks=2)
	dichotic_task_data = DichoticTaskData(exp, flow, dichotic_task_gui, dichotic_data_manager, data_manager, gui, menu, instructions_dichotic_break)
	
	# DCT-STP PRE AND POST:
	td_trainig = TaskData(menu, data_manager, sd, phase=DIGIT_PRE) # A class intance that organizes the data for the DCT task
	td_post_training = TaskData(menu, data_manager, sd, phase=DIGIT_POST) # A class intance that organizes the data for the DCT task
	dct_training = DctTask(gui, exp, td_trainig, flow) # A class intance that runs the DCT task
	dct_post_training = DctTask(gui, exp, td_post_training, flow) # A class intance that runs the DCT task
	
	# AFACT:
	afact_alternative = "shapes" # original/shapes/words
	atd = AfactTaskData(menu, data_manager, sd, phase=AFACT_PHASE)
	afact_task = AfactTask(gui, exp, atd, flow, afact_alternative=afact_alternative, words_objects=get_words_objects(WORDS_PATH))
	
	instructions_afact = Instructions(gui, exp, flow, IMAGEPATH_AFACT_INSTRUCTIONS) 
	instructions_afact_after_practice = Instructions(gui, exp, flow, IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE) 
	
	# MAB:
	mab_task_data = MABTaskData(menu, data_manager, sd, phase=MAB_PHASE) # A class intance that organizes the data for the DCT task
	mab_task = MABTask(gui, exp, mab_task_data, flow) # A class intance that runs the DCT task
	instructions_mab = Instructions(gui, exp, flow, IMAGEPATH_MAB_INSTRUCTIONS)
	instructions_mab_after_practice = Instructions(gui, exp, flow, IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC)
	
	# BMM:
	instructions_BMM = Instructions(gui, exp, flow, IMAGEPATH_BMM_INSTRUCTIONS)
	bmmtd = BMMTaskData(menu, data_manager, sd, phase=AFACT_PHASE) # intentionally this uses the AFACT phase name, so the same STPs allocation is done
	bmm_task = BMMTask(gui, exp, bmmtd, flow)
	
	# Body map & Emotions Raitings:
	body_map = ConsoleBodyMap(menu, flow, gui)
	
	# FLOW OF TASKS LIST:
	tasks = [
				lambda: menu.show(),
				lambda: dichotic_data_manager.__late_init__()   ,
				lambda: dichotic_task_data.__late_init__()      ,
				#
				#Body Maps & Emotions Raitings - Pre:
				#lambda: body_map.start_body_map_flow(),
				#
				# DCT-STP
				# lambda: instructions_dct_1.start_instrunctions(),
				# lambda: dct_training.start_task(), # practice 1 trials
				# lambda: instructions_dct_2.start_instrunctions(),
				# lambda: dct_training.start_task(), # practice 2 trials
				# lambda: instructions_dct_3.start_instrunctions(),
				# lambda: dct_training.start_task(), # real trials
				#
				#BMM:
				lambda: bmm_task.start_task(),
				#
				# MAB:
				lambda: instructions_mab.start_instrunctions(),
				lambda: mab_task.start_task(),
				lambda: instructions_mab_after_practice.start_instrunctions(),
				lambda: mab_task.start_task(),
				#
				# Afact:
				lambda: instructions_afact.start_instrunctions(),
				lambda: afact_task.start_task(), # practice trials
				lambda: instructions_afact_after_practice.start_instrunctions(),
				lambda: afact_task.start_task(), # real trials
				#
				# DCT-STP
				lambda: instructions_dct_1.start_instrunctions(),
				lambda: dct_post_training.start_task(), # practice 1 trials
				lambda: instructions_dct_2.start_instrunctions(),
				lambda: dct_post_training.start_task(), # practice 2 trials
				lambda: instructions_dct_3.start_instrunctions(),
				lambda: dct_post_training.start_task(), # real trials
				#
				lambda: instructions_dichotic_end.start_instrunctions(break_time=3000),
				#
				# Dichotic:
				lambda:instructions_dichotic_1.start_instrunctions(),
				lambda: dichotic_task_data.first_practice(side="Left"),				
				lambda: dichotic_task_data.first_practice(side="Right"),
				lambda:instructions_dichotic_2.start_instrunctions(),
				lambda: dichotic_task_data.second_practice(),
				lambda:instructions_dichotic_3.start_instrunctions(),
				lambda: dichotic_task_data.start_chunk(),
				lambda: instructions_end_of_experiment.start_instrunctions(),
				#
				#Body Maps & Emotions Raitings - Pre:
				#lambda: body_map.start_body_map_flow(),
				#
				
				]
	
	# EXPERIMENT FLOW HANDLER:
	flow.add_tasks(tasks)
	
	# SCREEN PROPERTIES:
	gui.bind("<space>", flow.next)
	gui.state('zoomed')
	#exp._full_screen_creator(gui) # for running in a complete full screen
	
	# EXECUTION OF THE PROGRAM
	exp.run()
	
if __name__ == "__main__":
	main()
