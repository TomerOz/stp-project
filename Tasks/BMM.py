from .DCT import DctTask
from playsound import playsound
import os 
import random

from .params import *

instructions_audio_path = r'.\\Tasks\\BMMRecordings'
instuctions_audio_1 = "BMM_1.m4a"
instuctions_audio_2 = "BMM_2.m4a"
instuctions_audio_3 = "BMM_3.m4a"
instuctions_audio_4 = "BMM_4.m4a"

class BMMTask(DctTask):
	def __init__(self, self, gui, exp, td, flow):
		super(BMMTask, self).__init__(gui, exp, td, flow, response_labels="original"):
		
		self.sentences_start_times = []
		
		self.instructions_paths = []
		self._read_instructions_audio_files()
	
	def _read_instructions_audio_files(self):
		instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_1)
		instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_2)
		instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_3)
		instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_4)
	
	def change_text_on_screen(self, text)
		self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=text)
	
	def display_main_frame(self, text=None):
		if text == None:
			text = "+"
		self.change_text_on_screen(text)
		self.exp.display_frame(FRAME_1, [LABEL_1])
	
	
	def play_instructions_audio(self, instuction_index):
		playsound(self.instructions_paths[instuction_index], block=False)
	

	
	def _start_audio(self):
		playsound(self.td.current_sentence_path, block=False) 						# audio is taken every trial from an updating filename 
		
		FIXED_BMM_INTERVAL = 1000
		random_noise = random.randint(200,800)
		interval_between_sentences = random_noise + FIXED_BMM_INTERVAL
		time_of_next_sentence = self.td.current_sentence.sentence_length + interval_between_sentences
		self.gui.after(time_of_next_sentence, self._continue)
		
	def _getresponse(self, eff=None, key=None):
		self.td.t1 = time.time()													## END OF TIME RECORD
		self.td.record_time()		
		self.key_pressed = key
		
		# unbinding keyboard - to not allow overriding sentences
		self._unbind_keyboard()
		self.td.record_trial(self.shown_num, self.key_pressed)

		# Practice feedback decision
		if self.td.current_trial_type_intance.is_practice:
			self._give_feedback(self.key_pressed)		
			self.gui.after(PRACTICE_FEEDBACK_DURATAION, self._continue) # TOMER - PAY ATTENTION TO THIS TIME
		else:
			self._continue()
	
	def _continue(self):
		self.td.current_trial += 1 # raising trial by 1 
		self.td.updata_current_sentence() # updatind sentence - loading everything nedded

		if self.td.current_trial_type_intance.is_change_block_trial:
			# pause on change block
			#self.change_block_frame()
			pass
		
		elif self.td.current_trial_type_intance.is_instructions:
			# next audio instructions
			#self.flow.next()
			pass
		else:
			self._trial() # continues to next trial	
	
	def _trial(self):
		'''This function is being called after response to last trial took place.
				First, it records last trial,
				Second, it start the next trial'''

		self.change_text_on_screen("+")
		
		# Checking if experiment ended:
		if self.td.current_trial < self.td.total_ammount_of_trials:
			''' Task is still running'''
			self.gui.after(0, self._start_audio)
		else:		
			''' Task is over'''
			self.gui.unbind(RIGHT_RESPONSE_KEY)
			self.gui.unbind(LEFT_RESPONSE_KEY)
			self.td.sd.create_data_frame()
			# raise flag of completion
			self.end_task()
			
	def _bind_keyboard(self):
		self.gui.unbind(CATCH_RIGHT_RESPONSE_KEY)
		self.gui.unbind(CATCH_LEFT_RESPONSE_KEY)
		self.gui.bind(RIGHT_RESPONSE_KEY, lambda eff: self._getresponse(eff, key=RIGHT))
		self.gui.bind(LEFT_RESPONSE_KEY, lambda eff: self._getresponse(eff,key=LEFT))
		
	def start_task(self, user_event=None):
		
		# ispect afact trial types - remove unrelevant
		# mind the differen inttruction phases
		# mind the different functions of pressing Space throughout the instructions/task
		
		# On task first initiation
		if self.td.current_trial == -1:
			self.td.event_timed_init() # user dependet initment of the dct data class
			self._create_task_label() # creating the main frame
			self.display_main_frame(text="+") # displaying main frame and setting text to fixation cross
			t1 = 0
			self.gui.after(t1, self._continue) # experiment was started
		
		# after instruction phase within this task
		else:
			self.exp.display_frame(FRAME_1, [LABEL_1])
			t1 = 0
			self.gui.after(t1, self._continue) # experiment was started
			