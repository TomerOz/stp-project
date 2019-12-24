import pygame as pg

from playsound import playsound

MAIN_FRAME = 'm_frame'
BACKGROUND_COLOR = 'black'
FIXATION_LABEL = 'fixation_label'
FIXATION_STIMULI = '+'
FIXATION_FONT = 'david 64 bold'
FOREGROUND_COLOR = 'white'

class DichoticOneBack(object):
	
	def __init__(self, gui, exp, data_manager):
		self.gui = gui
		self.exp = exp
		self.data_manager = data_manager
		
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
	
	AUDIOPATH = r'C:\Users\tomer\Desktop\dct_dichotic\Subjects'
	
	class Menu(object):
		def __init__(self, audiopath):
			self.audiopath = audiopath
			self.menu_data = {'gender':'','group':'','subject':1}
			self.updated_audio_path  = self.audiopath + '\\' + 'subject ' + str(self.menu_data['subject'])	
			
	menu = Menu(AUDIOPATH)
	data_manager = MainAudioProcessor()
	data_manager.__late_init__(menu)
	exp = Experiment()
	gui = exp.gui
	dichotic_instance = DichoticOneBack(gui, exp, data_manager)
	dichotic_instance._create_task_main_frame()
	gui.state('zoomed')# full screen with esc option
	
	gui.bind('<space>', dichotic_instance._play2tracks)
	exp.run()
	
	
if __name__ == "__main__":
	main()


		
		
		
		
		
		
		
		
		
		
#	create_frame(
#						
#						self, 
#						frame_name, # a string of frame name to save refference
#						parent=None,
#						full_screen=True,
#						background_color='gray'
#				):
#
#			
#	def create_label(
#					self, 
#					label_name, # a string of label name to save its refference
#					frame_name, 
#					label_text=None, 
#					label_fg='black', # letters color
#					label_bg='gray', # background color
#					label_font='david 28 bold',
#					label_justify='right',
#					label_width=None,
#					label_height=None,
#					blank_label=False,
#					image_label=False,
#					label_image=None,
#					anchor="center"
#				):
#
#
#
#
#
#
#
#
		