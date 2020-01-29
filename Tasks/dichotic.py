import pygame as pg
import ipdb
from playsound import playsound

MAIN_FRAME = 'm_frame'
BACKGROUND_COLOR = 'black'
FIXATION_LABEL = 'fixation_label'
FIXATION_STIMULI = '+'
FIXATION_FONT = 'david 64 bold'
FOREGROUND_COLOR = 'white'

NEGATIVE_SENTENCE = 'neg'			# According to audio df excel file
NEUTRAL_SENTENCE = 'ntr'			# According to audio df excel file
AFACT_PHASE = "afact_phase"


class DichoticOneBack(object):
	
	def __init__(self, gui, exp, data_manager, dichotic_data_manager):
		self.gui = gui
		self.exp = exp
		self.data_manager = data_manager
		
		self.dtd = DichoticTaskData(dichotic_data_manager, data_manager, gui)
		
	def _create_task_main_frame(self):
		'''creating main frame (GUI) and lable to present fixration stimuli'''
		self.exp.create_frame(MAIN_FRAME, background_color=BACKGROUND_COLOR)
		self.exp.create_label(FIXATION_LABEL, MAIN_FRAME, label_text=FIXATION_STIMULI, label_font=FIXATION_FONT, label_bg=BACKGROUND_COLOR, label_fg=FOREGROUND_COLOR)
		self.exp.display_frame(MAIN_FRAME,[FIXATION_LABEL])

	def _play2tracks(self, event=None):
		'''activating tow audio channels'''
		try_sound = self.data_manager.sentence_inittial_path + '\\' + self.data_manager.sentences[0].file_path
		pg.mixer.init(frequency=44000, size=-16,channels=2, buffer=4096)
		
		sound0 = pg.mixer.Sound(try_sound)
		
		channel0 = pg.mixer.Channel(0)
		channel1 = pg.mixer.Channel(1)
		
		# Play the sound (that will reset the volume to the default).
		channel0.play(sound0)
		
		# Now change the volume of the specific speakers.
		# The first argument is the volume of the left speaker and
		# the second argument is the volume of the right speaker.
		channel0.set_volume(1.0, 0.0)
		
		def x():
			channel1.set_volume(0.0, 1.0)
			channel1.play(sound0)
		self.gui.after(500, x)
		

class DichoticTaskData(object):
	def __init__(self, dichotic_data_manager, data_manager, gui):
		
		self.gui = gui
		self.data_manager = data_manager
		self.dichotic_data_manager = dichotic_data_manager
		
		# Task properties
		self.chunk_neu_start_delay	= 0
		self.chunk_neg_start_delay	= 300
		self.chunck_block_change_wait_time = 1000
		self.block_change_wait_time_addition = 1000
		
		# Dynamic Variables
		self.block = 0
		self.chunk = 1
		self.chunck_channels_completed_counter = 0 # On 2 it changes chunk
		self.chunk_end_trial = None
		
		self.global_trial = 0
		self.neu_trial = 0
		self.neg_trial = 0
		
		# initialization of current sentecne paths
		self._initialize_block_chunk()
		
		# Binding keyboard
		self.bind_keyboard()
		
		#Sound mixer initialization 
		pg.mixer.init(channels=6)
	
		# Creating left and right chanels
		self.neu_channel = pg.mixer.Channel(0)
		self.neg_channel = pg.mixer.Channel(7)		
		# right lef volumes of each channel
		self.left_neg	 = 1.0
		self.right_neg	 = 0.0
		self.left_neu	 = 0.0
		self.right_neu	 = 0.0
		
		self.valence_side = {"Right":"neu", "Left":"neg"} # will be updated in every Chunck Change # "Right" & "Left" are equivalent to event.keysym
		
		
	def _initialize_block_chunk(self):
		self.current_neu_sentence = self.dichotic_data_manager.blocks_dicts[self.block][self.chunk]["neu"][self.neu_trial] 
		self.current_neg_sentence = self.dichotic_data_manager.blocks_dicts[self.block][self.chunk]["neg"][self.neg_trial] 
		self.chunk_end_trial = len(self.dichotic_data_manager.blocks_dicts[self.block][self.chunk]["neg"])-1
	
	def get_response(self, event=None):
		if self.valence_side[event.keysym] == "neg":
			print self.current_neg_sentence.num
		elif self.valence_side[event.keysym] == "neu":
			print self.current_neu_sentence.num
	
	def bind_keyboard(self):
		self.gui.bind("<Right>", self.get_response)	
		self.gui.bind("<Left>", self.get_response)	
		
		
	def next_chunck_and_or_block(self):
		self.chunck_channels_completed_counter += 1
		if self.chunck_channels_completed_counter == 2:
			self.neu_trial = 0
			self.neg_trial = 0
			
			self.chunck_channels_completed_counter = 0
			self.chunk += 1
			print "Chunk {} Ended".format(str(self.chunk-1))
      
			if self.chunk == 4:
				self.next_block() # changing block, otherwise, still within the same block
			
			self._initialize_block_chunk()
			self.gui.after(self.chunck_block_change_wait_time, self.start_chunk)
		
		# Otherwise - Don't do anything
		
	def next_block(self):
		print "Chunk {} Ended"
		self.chunk = 0
		self.block += 1
		
	def start_chunk(self, event=None):
		self.gui.after(self.chunk_neu_start_delay, self.play_neu_sentence)
		self.gui.after(self.chunk_neg_start_delay, self.play_neg_sentence)
	
	def next_neu_trial(self):
		self.neu_trial += 1
		self.current_neu_sentence = self.dichotic_data_manager.blocks_dicts[0][self.chunk]["neu"][self.neu_trial] 
		
	def next_neg_trial(self):
		self.neg_trial += 1
		self.current_neg_sentence = self.dichotic_data_manager.blocks_dicts[0][self.chunk]["neg"][self.neg_trial]
	
	def play_neu_sentence(self):	
		print "neu - ",self.neu_trial, " ---- ", self.current_neu_sentence.num
		neu_sentence_sound_path = self.data_manager.sentence_inittial_path + '\\' + self.current_neu_sentence.file_path
		sound_neu = pg.mixer.Sound(neu_sentence_sound_path)
		self.neu_channel.set_volume(self.left_neu, self.right_neu)
		self.neg_channel.set_volume(self.left_neg, self.right_neg)
		self.neu_channel.play(sound_neu)
		self.neu_channel.set_volume(self.left_neu, self.right_neu)
		self.neg_channel.set_volume(self.left_neg, self.right_neg)
		
		self.gui.after(int(self.current_neu_sentence.sentence_length)+300, self.next_neu)
	
	def play_neg_sentence(self):
		print "neg - ",self.neg_trial, " ---- ", self.current_neg_sentence.num
		neg_sentence_sound_path = self.data_manager.sentence_inittial_path + '\\' + self.current_neg_sentence.file_path
		sound_neg = pg.mixer.Sound(neg_sentence_sound_path)
		self.neu_channel.set_volume(self.left_neu, self.right_neu)
		self.neg_channel.set_volume(self.left_neg, self.right_neg)
		self.neg_channel.play(sound_neg)
		self.neg_channel.set_volume(self.left_neg, self.right_neg)
		self.neu_channel.set_volume(self.left_neu, self.right_neu)
		
		self.gui.after(int(self.current_neg_sentence.sentence_length)+300, self.next_neg)
		
	def next_neu(self):
		if self.neu_trial < self.chunk_end_trial:
			self.next_neu_trial()
			self.play_neu_sentence()
		else:
			self.next_chunck_and_or_block()
		
	def next_neg(self):
		if self.neg_trial < self.chunk_end_trial:
			self.next_neg_trial()
			self.play_neg_sentence()
		else:
			self.next_chunck_and_or_block()
	 
def main():
	from ExGui import Experiment
	from processing.TasksAudioDataManager import MainAudioProcessor
	from processing.DichoticDataManager import DichoticTrialsManager
	from processing.wav_lengh import AudioProcessor
	from Data import SubjectData
	from ExpFlow import Flow
	from DCT import TaskData
	from OpeningMenu import Menu
	
	PRE_PROCESSED_AUDIO_DF = 'audio_data.xlsx'
	PROCESSED_AUDIO_DF = 'audio_data_digit.xlsx' # file name containing audio data after processing ready for dct-stp task
	SUBJECT = 'subject'
	GROUP = 'group'
	GENDER = 'gender'
	AUDIOPATH = r'Subjects'
	
	DICHOTIC_PHASE_STR = 'dichotic_phase' # a single name to be usef in both data_manager and dichotic data manager
	
	ap = AudioProcessor(PRE_PROCESSED_AUDIO_DF, PROCESSED_AUDIO_DF)
	exp = Experiment()
	gui = exp.gui
	sd = SubjectData()
	flow = Flow()
	
	data_manager = MainAudioProcessor(
										phases_names=[DICHOTIC_PHASE_STR, 'Post'], 
										n_trials_by_phase={DICHOTIC_PHASE_STR: 25,'Post': 40}, 
										n_practice_trials=4,
										dichotic_phase=DICHOTIC_PHASE_STR) #  phases_names=None, n_trials_by_phase=None, n_practice_trials=None):
	menu = Menu(exp, gui, flow, ap, AUDIOPATH, data_manager) # controls menu gui and imput fields
	menu.menu_data[SUBJECT] = 1 
	menu.menu_data[GROUP] = 1 
	menu.menu_data[GENDER] = 1
	
	
	dt = DichoticTrialsManager(data_manager, DICHOTIC_PHASE_STR)
	# lab
	menu.updated_audio_path	 = r"C:\Users\user\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	# mine
	menu.updated_audio_path	 = r"C:\Users\HP\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	# Alab
	menu.updated_audio_path	 = r"C:\Users\psylab6027\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	
	menu.ap.process_audio(menu.updated_audio_path) # process this subject audio files
	data_manager.__late_init__(menu)
	dt.__late_init__()
	
	
	#dichotic_task_data = TaskData(menu, data_manager, sd, phase=DICHOTIC_PHASE_STR, n_blocks=2)
	#dichotic_task_data.event_timed_init()
	
	#gui.bind("<Right>", change_feedback)	
	#gui.bind("<Left>", change_feedback)	
	
	
	gui = exp.gui
	dichotic_instance = DichoticOneBack(gui, exp, data_manager, dt)
	dichotic_instance._create_task_main_frame()
	gui.state('zoomed')# full screen with esc option
	
	gui.bind('<space>', dichotic_instance.dtd.start_chunk)
	#gui.bind('<space>', dichotic_instance._play2tracks)
	exp.run()
	
	
if __name__ == "__main__":
	main()
		