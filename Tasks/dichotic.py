import pygame as pg

from playsound import playsound

MAIN_FRAME = 'm_frame'
BACKGROUND_COLOR = 'black'
FIXATION_LABEL = 'fixation_label'
FIXATION_STIMULI = '+'
FIXATION_FONT = 'david 64 bold'
FOREGROUND_COLOR = 'white'

NEGATIVE_SENTENCE = 'neg' 			# According to audio df excel file
NEUTRAL_SENTENCE = 'ntr'			# According to audio df excel file
AFACT_PHASE = "afact_phase"


class DichoticOneBack(object):
	
	def __init__(self, gui, exp, data_manager, dichotic_data_manager):
		self.gui = gui
		self.exp = exp
		self.data_manager = data_manager
		
		
		# TEMP
		self.block = 0
		self.chunk = 1
		self.valence = "neg"
		self.dichotic_data_manager = dichotic_data_manager
		
		self.trial = 0
		self.current_neu_sentence = self.dichotic_data_manager.blocks_dicts[0][self.chunk]["neu"][self.trial].sentence 
		self.current_neg_sentence = self.dichotic_data_manager.blocks_dicts[0][self.chunk][self.valence][self.trial].sentence 
		## END TEMP
	
	def _create_task_main_frame(self):
		'''creating main frame (GUI) and lable to present fixration stimuli'''
		self.exp.create_frame(MAIN_FRAME, background_color=BACKGROUND_COLOR)
		self.exp.create_label(FIXATION_LABEL, MAIN_FRAME, label_text=FIXATION_STIMULI, label_font=FIXATION_FONT, label_bg=BACKGROUND_COLOR, label_fg=FOREGROUND_COLOR)
		self.exp.display_frame(MAIN_FRAME,[FIXATION_LABEL])
		
	
	
	#########
	def start_chunk(self, event):
		self.play_sentence()
	
	def next_trial(self):
		self.trial += 1
		self.current_neu_sentence = self.dichotic_data_manager.blocks_dicts[0][self.chunk]["neu"][self.trial].sentence 
		self.current_neg_sentence = self.dichotic_data_manager.blocks_dicts[0][self.chunk][self.valence][self.trial].sentence 
	
	def play_sentence(self):
		neu_sentence_sound_path = self.data_manager.sentence_inittial_path + '\\' + self.current_neu_sentence.file_path
		neg_sentence_sound_path = self.data_manager.sentence_inittial_path + '\\' + self.current_neg_sentence.file_path
		self.gui.after(0, lambda: playsound(neg_sentence_sound_path, block=False))
		self.gui.after(0, lambda: playsound(neu_sentence_sound_path, block=False))
		self.gui.after(int(self.current_neg_sentence.sentence_length)+300, self.next)
		
	def next(self):
		print self.trial
		self.next_trial()
		self.play_sentence()
	
	## DUBLE EVRY THING TO NEG AND NEU
	
	
	#########
	
	
	def _play2tracks(self, event=None):
		'''activating tow audio channels'''
		try_sound = self.data_manager.sentence_inittial_path + '\\' + self.data_manager.sentences[0].file_path
		pg.mixer.init(frequency=44000, size=-16,channels=2, buffer=4096)
		
		sound0 = pg.mixer.Sound(try_sound)
		
		channel0 = pg.mixer.Channel(0)
		channel1 = pg.mixer.Channel(1)
		channel2 = pg.mixer.Channel(2)

		# Play the sound (that will reset the volume to the default).
		channel0.play(sound0)
		
		# Now change the volume of the specific speakers.
		# The first argument is the volume of the left speaker and
		# the second argument is the volume of the right speaker.
		channel0.set_volume(1.0, 0.0)
		
		def x():
			channel1.play(sound0)
			channel1.set_volume(0.0, 1.0)
		self.gui.after(500, x)
		self.gui.after(1000, lambda : channel2.play(sound0))

	
	 
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
	menu.updated_audio_path  = r"C:\Users\user\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	# mine
	#menu.updated_audio_path  = r"C:\Users\HP\Documents\GitHub\stp-project" + "\\" + menu.audiopath + '\\' + 'subject ' + str(menu.menu_data[SUBJECT])	
	
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
	
	#gui.bind('<space>', dichotic_instance._play2tracks)
	gui.bind('<space>', dichotic_instance.start_chunk)
	exp.run()
	
	
if __name__ == "__main__":
	main()
		