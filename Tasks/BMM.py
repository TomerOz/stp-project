from .DCT import DctTask, TaskData
from playsound import playsound
import os 
import random
import librosa
import ipdb
import math
import time

from .params import *

INSTRUCTIONS_AUDIO_PATH = r'.\\Tasks\\BMMRecordings'
INSTUCTIONS_AUDIO_1 = "BMM_1.wav"
INSTUCTIONS_AUDIO_2 = "BMM_2.wav"
INSTUCTIONS_AUDIO_3 = "BMM_3.wav"
INSTUCTIONS_AUDIO_4 = "BMM_4.wav"
INSTUCTIONS_AUDIO_5 = "BMM_5.wav"


INSTRUCTION_1_DELAY = 1000
INSTRUCTION_2_DELAY = 1000
INSTRUCTION_3_DELAY = 1000
INSTRUCTION_4_DELAY = 1000
INSTRUCTION_5_DELAY = 1000
MIN_PRACTICE_RESPONSES = 0 # should be ~4

class BMMTask(DctTask):
	def __init__(self, gui, exp, td, flow):
		super(BMMTask, self).__init__(gui, exp, td, flow, response_labels="original")
		
		self.sentences_start_times = []
		
		self.instructions_paths = self._get_instructions_audio_files()
		self.n_instruction_audios = len(self.instructions_paths)
		self.instructions_input_delay_times = [INSTRUCTION_1_DELAY, INSTRUCTION_2_DELAY, INSTRUCTION_3_DELAY, INSTRUCTION_4_DELAY, INSTRUCTION_5_DELAY]
		self.instructions_audio_index = 0
		self.current_instruction_duration = self.get_duration_of_audio(self.instructions_audio_index)
		self.min_practice_responses = MIN_PRACTICE_RESPONSES 
		self.last_practice_response_times = []
		self.is_practice_finished = False
		self.is_stp_practice_finished = True
		self.current_sentence_responses = []
	
	def _get_instructions_audio_files(self):
		instructions_paths = []
		instructions_paths.append(os.path.join(INSTRUCTIONS_AUDIO_PATH, INSTUCTIONS_AUDIO_1))
		instructions_paths.append(os.path.join(INSTRUCTIONS_AUDIO_PATH, INSTUCTIONS_AUDIO_2))
		instructions_paths.append(os.path.join(INSTRUCTIONS_AUDIO_PATH, INSTUCTIONS_AUDIO_3))
		instructions_paths.append(os.path.join(INSTRUCTIONS_AUDIO_PATH, INSTUCTIONS_AUDIO_4))
		instructions_paths.append(os.path.join(INSTRUCTIONS_AUDIO_PATH, INSTUCTIONS_AUDIO_5))
		
		return instructions_paths
	
	def change_text_on_screen(self, text):
		self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=text)
	
	def display_main_frame(self, text=None):
		if text == None:
			text = "+"
		self.change_text_on_screen(text)
		self.exp.display_frame(FRAME_1, [LABEL_1])
	
	
	def play_instructions_audio(self, instuction_index):
		playsound(self.instructions_paths[instuction_index], block=False)
		self.td.start_time_record() # saves t0 - when instructions starts
	
	def _start_audio(self):
		playsound(self.td.current_sentence_path, block=False) 						# audio is taken every trial from an updating filename 
		self.td.start_time_record() # saves t0 - when sentence starts
		
		if False:
			# In case we want senetnces to follow each other automatically:
			FIXED_BMM_INTERVAL = 1000
			random_noise = random.randint(200,800)
			interval_between_sentences = random_noise + FIXED_BMM_INTERVAL
			time_of_next_sentence = self.td.current_sentence.sentence_length + interval_between_sentences
			self.gui.after(time_of_next_sentence, self._continue)
		
	def _getresponse(self, eff=None):
		self.td.t1 = time.time() # recording rt								## END OF TIME RECORD
		self.td.record_time()
		self.td.record_trial()
		
		self.current_sentence_responses.append(self.td.t1)
		## TODO: write another td child class that handels such record time
		## TODO: manage data saving
		
		if self.is_practice_finished:
			# check if we can continue
			if len(self.current_sentence_responses) > 3:
				self.current_sentence_responses = []
				self._continue()
				
		else:
			self.last_practice_response_times.append(self.td.t1)
	
	def _continue(self):
		self.td.current_trial += 1 # raising trial by 1 
		self.td.updata_current_sentence() # updatind sentence - loading everything nedded
		
		self.current_sentence_responses = [] # clearing for next sentence
		
		if self.td.current_trial_type_intance.is_change_block_trial:
			# pause on change block
			#self.change_block_frame()
			pass
		
		elif self.td.current_trial_type_intance.is_instructions:
			# next audio instructions
			#self.flow.next()
			pass
		
		elif self.td.current_trial == 5 and not self.is_stp_practice_finished: # end of practice stps back to instructions
			self.is_practice_finished = False
			self._unbind_keyboard()
			self.gui.after(1000, self.next_audio_instructions)
		else:
			self._trial() # continues to next trial	
	
	def _trial(self):
		'''This function is being called after response to last trial took place.
				First, it records last trial,
				Second, it start the next trial'''

		self.change_text_on_screen("+")
		self._bind_keyboard()
		# Checking if experiment ended:
		if self.td.current_trial < self.td.total_ammount_of_trials:
			''' Task is still running'''
			self.gui.after(0, self._start_audio)
		else:		
			''' Task is over'''
			self._unbind_keyboard()
			self.td.sd.create_data_frame()
			# raise flag of completion
			self.end_task()
	
	def _unbind_keyboard(self):
		self.gui.unbind(CATCH_RIGHT_RESPONSE_KEY)
		self.gui.unbind(CATCH_LEFT_RESPONSE_KEY)
		self.gui.unbind(RIGHT_RESPONSE_KEY)
		self.gui.unbind(LEFT_RESPONSE_KEY)
		self.gui.unbind(BMM_RESPONSE_KEY)
		### TODO: Make sure to unbind here all other tasks keys!! #### <><><>
	
	def _bind_keyboard(self):
		self.gui.bind(BMM_RESPONSE_KEY, lambda eff: self._getresponse(eff))
		
	def get_duration_of_audio(self, instuction_index):
		duration = 1000*math.ceil(float(librosa.get_duration(filename=self.instructions_paths[instuction_index])))
		return duration
		
	def _get_input_delay_time(self):
		return self.instructions_input_delay_times[self.instructions_audio_index]
	
	def start_over_instructions_audio(self):
		self.exp.display_frame(FRAME_1, [LABEL_1])
		# to avoid re evoking the replay button
		self.exp.LABELS_BY_FRAMES["message_invalid_frame"]['message_invalid_label'].destroy()
		self.start_audio_instructions()
		
	def _on_invalidated_phase(self):
		invalid_frame = self.exp.create_frame("message_invalid_frame")
		message_invalid_label = self.exp.create_label("message_invalid_label", "message_invalid_frame")
		button_hear_practice_again = self.exp.create_button("message_invalid_frame", "message_invalid_label", u"שמע הוראות שוב", self.start_over_instructions_audio)
		self.exp.display_frame("message_invalid_frame", ["message_invalid_label"])
				
	def validation_post_practice_instructions(self):
		if self.instructions_audio_index == 0:
			self.last_practice_response_times = []
			return True
		elif self.instructions_audio_index == 1:
			if len(self.last_practice_response_times) >= self.min_practice_responses:
				self.last_practice_response_times = []
				return True
		elif self.instructions_audio_index == 2:
			if len(self.last_practice_response_times) >= self.min_practice_responses:
				self.last_practice_response_times = []
				return True
		elif self.instructions_audio_index == 3:
			if len(self.last_practice_response_times) >= self.min_practice_responses:
				self.last_practice_response_times = []
				return True
			
		return False
	
	def next_audio_instructions(self):
		self._unbind_keyboard()
		if self.validation_post_practice_instructions():
			self.instructions_audio_index += 1
			self.start_audio_instructions()
		elif self.instructions_audio_index == 4: # audio_phase ended
			self.is_practice_finished = True
			self.is_stp_practice_finished = True
			self.td.current_trial -=1 #giving back the lost trial that was the stp practice end marker
			self._continue() # experiment starts
		else:
			self._on_invalidated_phase()
			# some message - repeat - inform experimenter				
			
	def start_audio_instructions(self):
		self.play_instructions_audio(self.instructions_audio_index)
		self.gui.after(self._get_input_delay_time(), self._bind_keyboard)
		if self.instructions_audio_index < self.n_instruction_audios:
			if self.instructions_audio_index == 3: # continue to stps practice:
				self.is_practice_finished = True # temporary
				self.gui.after(self.current_instruction_duration, self._continue) # experiment starts
			
			else: # continue to next instructions
				self.current_instruction_duration = self.get_duration_of_audio(self.instructions_audio_index)
				self.gui.after(self.current_instruction_duration, self.next_audio_instructions)
		# else:
			# self.is_practice_finished = True
			# self.gui.after(self.current_instruction_duration, self._continue) # experiment starts
			
	def start_task(self, user_event=None):
		# mind the differen inttruction phases
		# mind the different functions of pressing Space throughout the instructions/task
		
		# On task first initiation
		if self.td.current_trial == -1:
			self.td.event_timed_init() # user dependet initment of the dct data class
			
			self._create_task_label() # creating the main frame
			self.display_main_frame(text="+") # displaying main frame and setting text to fixation cross
			
			# starting audio instructions:
			self.td.updata_current_sentence() # such that any sentence object will be found for data saving
			self._unbind_keyboard()
			t1 = 0
			self.gui.after(t1, self.start_audio_instructions)
			#self.gui.after(t1, self._continue) # experiment was started
		
		# after instruction phase within this task
		elif self.is_practice_finished:
			self.exp.display_frame(FRAME_1, [LABEL_1])
			t1 = 0
			self.gui.after(t1, self._continue) # experiment was started

class BMMTaskData(TaskData):
	def __init__(self, menu, data_manager, subject_data, phase=None, sessions_names=None):
		super(BMMTaskData, self).__init__(menu, data_manager, subject_data, phase=phase, sessions_names=sessions_names)
		
	def record_time(self):
		self.last_RT = self.t1 # not actually RT but a response time stamp
		
	def record_trial(self):
		# saving key press in order to pass into Data package
		self.num_shown_type = None
		self.is_catch_trial = False
		self.correct = None
		self.last_trial_classification = None
		self.last_key_pressed = "Space"
		self.trial_phase = self.current_trial_type_intance.trial_phase
		
		# saving data 
		self.sd.push_data_packge(self)
	
	def event_timed_init(self):
		super(BMMTaskData, self).event_timed_init()
		# filttering our instructions,change block and feefback trials
		self.trials_types_by_phase = self.filter_td_trial_types_for_BMM()
		ipdb.set_trace()
	
	def filter_td_trial_types_for_BMM(self):
		filtered_trial_types = [tp for tp in self.trials_types_by_phase \
									if not tp.is_instructions \
									and not tp.is_afact_feedback \
									and not tp.is_change_block_trial]
		return filtered_trial_types
	