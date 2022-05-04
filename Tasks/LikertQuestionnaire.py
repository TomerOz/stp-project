
from params import *
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

		self.scales_ranges = [11, 11]
		self.questions = ["שאלה 1", "שאלה 2"]
		self.ends = [("גבוה","נמוך"),("דומה","לא דומה")]

		self.buttons_labels_names = []
		self.questions_labels_names = []
		self.ends_labels_names = []

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
			self.exp.create_label(label_heigh_name, FRAME_1, label_text=self.ends[0], label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")
			self.exp.create_label(label_low_name, FRAME_1, label_text=self.ends[1], label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")
			self.exp.create_label(label_buttons_name, FRAME_1, label_text="", label_fg=FOREGROUND, label_bg=BACKGROUND, label_font=FONT, label_justify="center")

	def create_likert_buttons(self):
		for i, bl_name in enumerate(self.buttons_labels_names):
			for button in range(self.scales_ranges[i]):
				self.exp.create_button(FRAME_1, bl_name, button, self._choose_likert_number, button_width=8, pack_style="left", button_name=bl_name+"_"+str(button))



		'''
		button_name=None,
		button_width=None,
		button_height=None
		'''

	def _choose_likert_number(self):
		pass
	def _update_label_positions_according_to_button(self, button_name, label_name):
		x, y = type(self.exp).BUTTONS[button_name].winfo_rootx(), type(self.exp).BUTTONS[button_name].winfo_rooty()
		bw = type(self.exp).BUTTONS[button_name].winfo_width()
		lw = type(self.exp).LABELS_BY_FRAMES[FRAME_1][label_name].winfo_width()
		lh = type(self.exp).LABELS_BY_FRAMES[FRAME_1][label_name].winfo_height()
		type(self.exp).LABELS_BY_FRAMES[FRAME_1][label_name].place(x=x+bw/2, y=y-lh)
		self.gui.unbind("<space>")

	def pre_run(self):
		self._create_task_label()
		self.create_likert_buttons()
		self.exp.display_frame(FRAME_1, self.buttons_labels_names+self.questions_labels_names+self.ends_labels_names)
		self.gui.after(10,self.flow.next)

	def run_task(self):
		ipdb.set_trace()
		self._update_label_positions_according_to_button("q0b", "lh0")
		self._update_label_positions_according_to_button("q0b", "ll0")


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
