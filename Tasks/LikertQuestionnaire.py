
from .params import *
import pandas as pd
import os
import ipdb

LABEL_2 = "LABEL_2"
LABEL_3 = "LABEL_3"
LABEL_4 = "LABEL_4"
FONT = 'Courier 22 bold'
class LikertQuestion(object):
	def __init__(self, gui, exp, flow):
		self.exp = exp
		self.gui = gui
		self.flow = flow

		self.scales_ranges = [10, 10]
		self.q1 = "?בין 1 ל-10, באיזה מידה הרגשת שהזדהת עם המשפטים ששמעת \n (כאשר 1 = כלל לא, ו-10 = במידה רבה מאוד)"
		self.q2 = "?בין 1 ל-10, באיזה מידה הרגשת שהמשפטים דומים למחשבות שעוברות לך בראש \n (כאשר 1 = כלל לא, ו-10 = במידה רבה מאוד)"
		self.questions = [self.q1, self.q2]
		self.high_heb = "במידה רבה מאוד"
		self.low_heb = "כלל לא"
		self.ends = [[self.high_heb,self.low_heb],[self.high_heb,self.low_heb]]

		self.buttons_labels_names = []
		self.questions_labels_names = []
		self.ends_labels_names = []
		self.answers = {}
		self.answers_names = ["IdentificationWithThoughts", "SimilarityToThoughts"]

	def _create_task_label(self):
		self.exp.create_frame(
								FRAME_1,
								full_screen=False,
								background_color=BACKGROUND
								)
		for i in range(len(self.questions)):
			label_heigh_name = "lh"+str(i)
			label_low_name = "ll"+str(i)
			label_question_name = "q"+str(i)
			label_buttons_name = "q"+str(i)+"b"
			self.ends_labels_names.append((label_heigh_name,label_low_name))
			self.questions_labels_names.append(label_question_name)
			self.buttons_labels_names.append(label_buttons_name)

			self.exp.create_label(label_question_name, FRAME_1, label_text=self.questions[i], label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")
			self.exp.create_label(label_heigh_name, FRAME_1, label_text=self.ends[i][0], label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")
			self.exp.create_label(label_low_name, FRAME_1, label_text=self.ends[i][1], label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")
			self.exp.create_label(label_buttons_name, FRAME_1, label_text="", label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")
		self.exp.create_label("end_button_label", FRAME_1, label_text="", label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")

	def _end_task(self):
		output_path = r'Tasks\bodymap\output'
		pd.DataFrame(self.answers).to_excel(os.path.join(output_path,"Identification.xlsx"), index=False)
		self.flow.next()

	def _choose_likert_number(self,question, num):
		self.answers[self.answers_names[question]] = [num]
		for button in range(self.scales_ranges[question]):
			button_name = self.buttons_labels_names[question]+"_"+str(button+1)
			type(self.exp).BUTTONS[button_name].config(relief="raised", bg="white")
		button_name = self.buttons_labels_names[question]+"_"+str(num)
		type(self.exp).BUTTONS[button_name].config(relief="sunken", bg="green")

	def create_likert_buttons(self):
		for i, bl_name in enumerate(self.buttons_labels_names):
			for button in range(self.scales_ranges[i]):
				self.exp.create_button(FRAME_1, bl_name, button+1, lambda n=button+1, q=i: self._choose_likert_number(q,n), button_width=8, pack_style="left", button_name=bl_name+"_"+str(button+1))

	def _update_label_positions_according_to_button(self, button_name, label_name,space_direction):
		x, y = type(self.exp).BUTTONS[button_name].winfo_rootx(), type(self.exp).BUTTONS[button_name].winfo_rooty()
		bw = type(self.exp).BUTTONS[button_name].winfo_width()
		bh = type(self.exp).BUTTONS[button_name].winfo_height()
		lw = type(self.exp).LABELS_BY_FRAMES[FRAME_1][label_name].winfo_width()
		lh = type(self.exp).LABELS_BY_FRAMES[FRAME_1][label_name].winfo_height()
		type(self.exp).LABELS_BY_FRAMES[FRAME_1][label_name].place(x=x+(space_direction*bw/2), y=y-65)
		self.gui.unbind("<space>")

	def pre_run(self):
		self._create_task_label()
		self.create_likert_buttons()
		self.exp.create_button(FRAME_1, "end_button_label", "סיום", self._end_task, button_width=8, button_name="end button")
		labels_oreder = []
		for i in range(len(self.buttons_labels_names)):
			labels_oreder.append(self.questions_labels_names[i])
			labels_oreder.append(self.buttons_labels_names[i])
		self.exp.display_frame(FRAME_1, labels_oreder + ["end_button_label"])
		self.gui.after(10,self.flow.next)
		# +self.questions_labels_names
		#+ends_labels_names_flat
	def run_task(self):
		ends_labels_names_flat = [item for sublist in self.ends_labels_names for item in sublist]
		self._update_label_positions_according_to_button("q0b_10", "lh0", 1)
		self._update_label_positions_according_to_button("q0b_1", "ll0", -1)
		self._update_label_positions_according_to_button("q1b_10", "lh1", 1)
		self._update_label_positions_according_to_button("q1b_1", "ll1", -1)
		self.exp.un_hide_cursor()


def main():
	from ExGuiForER import Experiment
	from Tasks.ExpFlow import Flow

	exp = Experiment() # A class instance of experiments buildind
	gui	 = exp.EXPERIMENT_GUI # the gui object the above mentioned class
	flow = Flow()

	lq = LikertQuestion(gui, exp, flow)

	tasks = [lambda: lq.pre_run(),
			lambda: lq.run_task(),
			]

	flow.add_tasks(tasks)
	gui.bind("<space>",flow.next)
	gui.state('zoomed')

	exp.run()

if __name__ == '__main__':
	main()





'''

self.alternative_task_canvas.delete("all")
width = 40
height = 40
space = 10
#start = round((self.alternative_task_canvas_width - ((n*(width+space))-space))/2)
#y_start = self.alternative_task_canvas_hight/2 - height/2
#for n_shapes in range(n):
#	self.alternative_task_canvas.create_rectangle(start+n_shapes*(width+space),y_start,start+n_shapes*(width+space)+width,height+y_start, fill="white")

n_in_row = 3
start = round((self.alternative_task_canvas_width - ((n_in_row*(width+space))-space))/2)
y_start_row_2 = self.alternative_task_canvas_hight/2 - height/2
y_start_row_1 = y_start_row_2 - height - space
y_start_row_3 = y_start_row_2 + height + space
colors = ["black"]*9
for i in random.sample(list(range(9)), n):
	colors[i]="white"
for n_shapes in range(n_in_row):
	self.alternative_task_canvas.create_rectangle(start+n_shapes*(width+space),y_start_row_1,start+n_shapes*(width+space)+width,height+y_start_row_1, fill=colors[n_shapes], outline='white')


'''
