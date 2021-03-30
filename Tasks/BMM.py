from .DCT import DctTask
from playsound import playsound
import os 
import random
import librosa
import ipdb
import math

from .params import *

instructions_audio_path = r'.\\Tasks\\BMMRecordings'
instuctions_audio_1 = "BMM_1.wav"
instuctions_audio_2 = "BMM_2.wav"
instuctions_audio_3 = "BMM_3.wav"
instuctions_audio_4 = "BMM_4.wav"

class BMMTask(DctTask):
	def __init__(self, gui, exp, td, flow):
		super(BMMTask, self).__init__(gui, exp, td, flow, response_labels="original")
		
		self.sentences_start_times = []
		
		self.instructions_paths = []
		self._read_instructions_audio_files()
		
		self.is_practice_finished = False
		self.n_instruction_audios = 4 # equvalent to len(self.instructions_paths)
		self.instructions_audio_index = 0
		self.current_instruction_duration = self.get_duration_of_audio(self.instructions_audio_index)
		self.last_practice_response_times = []
	
	def _read_instructions_audio_files(self):
		self.instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_1))
		self.instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_2))
		self.instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_3))
		self.instructions_paths.append(os.path.join(instructions_audio_path, instuctions_audio_4))
	
	def change_text_on_screen(self, text):
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
		self.td.start_time_record()
		
		if False:
			# In case we want senetnces to follow each other automatically:
			FIXED_BMM_INTERVAL = 1000
			random_noise = random.randint(200,800)
			interval_between_sentences = random_noise + FIXED_BMM_INTERVAL
			time_of_next_sentence = self.td.current_sentence.sentence_length + interval_between_sentences
			self.gui.after(time_of_next_sentence, self._continue)
		
	def _getresponse(self, eff=None):
		self.td.t1 = time.time() # recording rt								## END OF TIME RECORD
		former_t0 = self.td.t0
		self.td.t0 = self.td.t1 # updating t0
		
		if self.is_practice_finished:
		
			self.td.record_time()		
			
			# unbinding keyboard - to not allow overriding sentences
			self._unbind_keyboard()
			self.td.record_trial() ## TODO: write another td child class that handels such record time

			# Practice feedback decision
			if self.td.current_trial_type_intance.is_practice:
				self._give_feedback(self.key_pressed)		
				self.gui.after(PRACTICE_FEEDBACK_DURATAION, self._continue) # TOMER - PAY ATTENTION TO THIS TIME
			else:
				self._continue()
		else:
			self.last_practice_response_times.append(self.td.t1-former_t0)
	
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
			ipdb.set_trace()
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
	
	def _unbind_keyboard(self):
		self.gui.unbind(CATCH_RIGHT_RESPONSE_KEY)
		self.gui.unbind(CATCH_LEFT_RESPONSE_KEY)
		self.gui.unbind(RIGHT_RESPONSE_KEY)
		self.gui.unbind(LEFT_RESPONSE_KEY)
		self.gui.unbind(BMM_RESPONSE_KEY)
		### TODO: Make sure to unbind here all other tasks keys!! #### <><><>
	
	def _bind_keyboard(self):
		self.gui.bind(BMM_RESPONSE_KEY, lambda eff: self._getresponse(eff))
		
	def filter_td_trial_types_for_BMM(self):
		filtered_trial_types = [tp for tp in self.td.trials_types_by_phase \
									if not tp.is_instructions \
									and not tp.is_afact_feedback \
									and not tp.is_change_block_trial]
		return filtered_trial_types
	
	def get_duration_of_audio(self, instuction_index):
		duration = 1000*math.ceil(float(librosa.get_duration(filename=self.instructions_paths[instuction_index])))
		return duration
		
	def validation_post_practice_instructions(self):
		if self.instructions_audio_index == 0:
			self.last_practice_response_times = []
			ipdb.set_trace()
			return True
		elif self.instructions_audio_index == 1:
			ipdb.set_trace()
			if len(self.last_practice_response_times) > 3:
				return True
		elif self.instructions_audio_index == 2:
			ipdb.set_trace()
				
			
		return False
	
	def next_audio_instructions(self):
		if self.validation_post_practice_instructions():
			self.instructions_audio_index += 1
			self.current_instruction_duration = self.get_duration_of_audio(self.instructions_audio_index)
			self.start_audio_instructions()
		else:
			self.start_audio_instructions()
			# some message - repeat - inform experimenter
			
	
	def start_audio_instructions(self):
		self.play_instructions_audio(self.instructions_audio_index)
		if self.instructions_audio_index < self.n_instruction_audios:
			self.gui.after(self.current_instruction_duration, self.next_audio_instructions)
		else:
			self.is_practice_finished = True
			self.gui.after(self.current_instruction_duration, self._continue) # experiment starts
			
	def start_task(self, user_event=None):
		# mind the differen inttruction phases
		# mind the different functions of pressing Space throughout the instructions/task
		
		# On task first initiation
		if self.td.current_trial == -1:
			self.td.event_timed_init() # user dependet initment of the dct data class
			self.td.trials_types_by_phase = self.filter_td_trial_types_for_BMM() # filttering our instructions,change block and feefback trials
			self._create_task_label() # creating the main frame
			self.display_main_frame(text="+") # displaying main frame and setting text to fixation cross
			
			t1 = 0
			self.gui.after(t1, self.start_audio_instructions)
			#self.gui.after(t1, self._continue) # experiment was started
		
		# after instruction phase within this task
		elif self.is_practice_finished:
			self.exp.display_frame(FRAME_1, [LABEL_1])
			t1 = 0
			self.gui.after(t1, self._continue) # experiment was started
			