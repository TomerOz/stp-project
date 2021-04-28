
from .DCT import DctTask, TaskData
from .params import *
import time


class MABTask(DctTask):
	def __init__(self, gui, exp, td, flow, response_labels=None):
		super().__init__(gui, exp, td, flow, response_labels=response_labels)
	
	def _getresponse_mab(self, eff=None):
		self_caught = time.time() 
		self.td.self_caught_in_trial = self_caught # will contain the last button press in each trial
		self.td.self_caught_list.append(self_caught)
		if self.td.current_trial_type_intance.trial_phase == "MAB practice":
			self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=MAB_FEEDBACK_TEXT))
			self.gui.after(MAB_PRACTICE_FEEDBACK_DURATAION, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][LABEL_1].config(text=self.stimulus_live_text)) # text feedback

	def start_task(self, user_event=None):
		self.gui.bind(MAB_RESONSE_KEY, lambda eff: self._getresponse_mab(eff))
		super().start_task(user_event=user_event)
	
	def end_task(self):
		self.gui.unbind(MAB_RESONSE_KEY)
		super().end_task()
		
class MABTaskData(TaskData):
	def __init__(self, menu, data_manager, subject_data, phase=None, sessions_names=None):
		super().__init__(menu, data_manager, subject_data, phase=phase, sessions_names=sessions_names)
		
		self.self_caught_in_trial = None # will contain the last button press in each trial
		self.self_caught_list = [] # in each trial will conatin a python growing list
									# good for multpile presses in each trial