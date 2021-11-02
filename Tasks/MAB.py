
from .DCT import DctTask, TaskData
from .params import *
import time
import ipdb



class MABTask(DctTask):
	def __init__(self, gui, exp, td, flow, response_labels=None):
		super().__init__(gui, exp, td, flow, response_labels=response_labels)

		self.inter_trial_interval = MAB_INTER_TRIAL_INTERVAL

	def _getresponse_mab(self, eff=None):
		self_caught = time.time()
		self.td.self_caught_in_trial = self_caught # will contain the last button press in each trial
		self.td.self_caught_list.append(self_caught)
		self.show_mab_space_press_feedback()

	def show_mab_space_press_feedback(self, eff=None):
		self.gui.after(0, lambda:self.exp.hide_frame(FRAME_1))
		self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][MAB_FEEDBACK_LABEL].pack())
		if self.td.current_trial_type_intance.trial_phase == "MAB practice":
			self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][MAB_FEEDBACK_LABEL].config(text="\n" +MAB_FEEDBACK_TEXT + "\n" + "___",font=("Courier", 30)))
			self.gui.after(0, lambda:self.exp.display_frame(FRAME_1, [LABEL_1, MAB_FEEDBACK_LABEL], use_place={MAB_FEEDBACK_LABEL: [self.exp.cx,self.exp.cy+55]}))
			self.gui.after(MAB_PRACTICE_FEEDBACK_DURATAION, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][MAB_FEEDBACK_LABEL].config(text=""))
		else:
			self.gui.after(0, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][MAB_FEEDBACK_LABEL].config(text="___"))
			self.gui.after(0, lambda:self.exp.display_frame(FRAME_1, [LABEL_1, MAB_FEEDBACK_LABEL], use_place={MAB_FEEDBACK_LABEL: [self.exp.cx,self.exp.cy+30]}))
			self.gui.after(MAB_FEEDBACK_DURATAION, lambda:self.exp.LABELS_BY_FRAMES[FRAME_1][MAB_FEEDBACK_LABEL].config(text=""))

	def start_task(self, user_event=None):
		self.gui.bind(MAB_RESONSE_KEY, lambda eff: self._getresponse_mab(eff))
		super().start_task(user_event=user_event)
		self.exp.create_label(MAB_FEEDBACK_LABEL, FRAME_1, label_text="____", label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=DCT_STIMULI_FONT, label_justify="center")

	def end_task(self):
		self.gui.unbind(MAB_RESONSE_KEY)
		self.exp.LABELS_BY_FRAMES[FRAME_1][MAB_FEEDBACK_LABEL].destroy()
		super().end_task()

class MABTaskData(TaskData):
	def __init__(self, menu, data_manager, subject_data, phase=None, sessions_names=None):
		super().__init__(menu, data_manager, subject_data, phase=phase, sessions_names=sessions_names)

		self.self_caught_in_trial = None # will contain the last button press in each trial
		self.self_caught_list = [] # in each trial will conatin a python growing list
									# good for multpile presses in each trial
