import tkinter as tk
from ExGuiTempAfact import Experiment
from PIL import Image, ImageTk
import ipdb

exp = Experiment() # A class instance of experiments buildind
gui  = exp.EXPERIMENT_GUI # the gui object the above mentioned class
MAIN_FRAME = "af"
FEEDBACK_LABEL = "al"

ALTERNATIVE_TASK_FRAME = "alternative_task_frame"
ALTERNATIVE_TASK_LABEL = "alternative_task_label"

class DummyClass(object):
	def __init__(self, gui, exp, width=500, height=600, max_bias_z_score=None):
		self.gui = gui
		self.exp = exp
		self.width = width
		self.height = height
		self.feedback_canvas = None # Will be later created
		self.ammount_of_ticks = 10
		self.max_bias_z_score = 3.0
		
		self.feedback_scale_pic = r'AFACTStimuliPictures\FeedbackScale_2.png'
		self.feedback_arrow_pic = r'AFACTStimuliPictures\FeedbackArrow.png'
				
		self.scale_resize_factor = 1.8
		self.arrow_resize_factor = 0.8
		
		self.scale_top_tick = 23*self.scale_resize_factor # in px, extracted from microspft "paint" and referrs to this file -> feedback_scale_pic
		self.scale_bottom_tick = 252*self.scale_resize_factor # in px
		
		self.scale_y_location = 0
		self.length_of_feedback = self.scale_bottom_tick - self.scale_top_tick
		
		self.create_feedback_canvas_orginal()
		self.create_alternative_task_canvas()

	def create_alternative_task_canvas(self):
		self.exp.create_frame(ALTERNATIVE_TASK_FRAME)
		self.exp.create_label(ALTERNATIVE_TASK_LABEL, ALTERNATIVE_TASK_FRAME)
		label_ref = self.exp.LABELS_BY_FRAMES[ALTERNATIVE_TASK_FRAME][ALTERNATIVE_TASK_LABEL]
		
		self.alternative_task_canvas = self.exp.tk_refference.Canvas(label_ref, width=400, height=100, bg="white", highlightbackground="black")
		self.alternative_task_canvas.create_rectangle(0,0,40,40, fill="grey")
		self.alternative_task_canvas.pack(expand=self.exp.tk_refference.YES, fill=self.exp.tk_refference.BOTH)
	
	def create_feedback_canvas_orginal(self):

		self.exp.create_frame(MAIN_FRAME)
		self.exp.create_label(FEEDBACK_LABEL, MAIN_FRAME)
		feedback_label_ref = self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL]
		
		
		self.feedback_canvas = self.exp.tk_refference.Canvas(feedback_label_ref, width=self.width, height=self.height, bg="Black", highlightbackground="black")
		self.y_middle = self.height/2 # inorder ti nake it 0 to 100
		self.x_middle = self.width/2.0
		
		# load the .gif image file
		self.feesback_scale = Image.open(self.feedback_scale_pic)
		self.feesback_scale = self.feesback_scale.resize(
														(int(self.feesback_scale.width*self.scale_resize_factor),
														int(self.feesback_scale.height*self.scale_resize_factor)), 
														Image.ANTIALIAS)
		self.feesback_scale = ImageTk.PhotoImage(self.feesback_scale)
		
		
		# put gif image on canvas
		# pic's upper left corner (NW) on the canvas is at x=50 y=10
		scale_height = self.feesback_scale.height()
		scale_width = self.feesback_scale.width()
		scale_half_width =  scale_width/2.0
		scale_half_hight =  scale_height/2.0
		nw_scale_anchor_x = self.x_middle - scale_half_width 
		self.scale_y_location = self.y_middle-scale_half_hight
		self.feedback_canvas.create_image(nw_scale_anchor_x, self.scale_y_location, image=self.feesback_scale, anchor=self.exp.tk_refference.NW)
		
		#self.feedback_arrow = self.exp.tk_refference.PhotoImage(file=self.feedback_arrow_pic)
		self.feedback_arrow = Image.open(self.feedback_arrow_pic)
		self.feedback_arrow = self.feedback_arrow.resize(
														(int(self.feedback_arrow.width*self.arrow_resize_factor),
														int(self.feedback_arrow.height*self.arrow_resize_factor)),
														Image.ANTIALIAS)
		self.feedback_arrow = ImageTk.PhotoImage(self.feedback_arrow)
		feedback_arrow_height = self.feedback_arrow.height()
		feedback_arrow_width = self.feedback_arrow.width()
		
		self.arrow_y = self.scale_y_location + self.scale_top_tick - feedback_arrow_height/2.0 # equvalent to no bias at all
		self.arrow_x = scale_width+nw_scale_anchor_x
		self.feedback_canvas.create_image(self.arrow_x, self.arrow_y, image=self.feedback_arrow, anchor=self.exp.tk_refference.NW, tags='FeedbackArrow')

		self.feedback_canvas.pack(expand=self.exp.tk_refference.YES, fill=self.exp.tk_refference.BOTH)
	
	def create_feedback_original(self, bias_z_score):
		
		gui = self.gui
		if bias_z_score <=0:
			bias_z_score = 0
		
		relative_bias = bias_z_score/self.max_bias_z_score
		
		if relative_bias >= 1.0:
			relative_bias = 1.0
			
		y_feedback = relative_bias*self.length_of_feedback
		self.feedback_canvas.delete("FeedbackArrow")
		self.feedback_canvas.create_image(self.arrow_x, self.arrow_y+y_feedback, image=self.feedback_arrow, anchor=self.exp.tk_refference.NW, tags="FeedbackArrow")
		

dc = DummyClass(gui, exp)
#dc.create_feedback_canvas_orginal()
#exp.display_frame(MAIN_FRAME, [FEEDBACK_LABEL])
exp.display_frame(ALTERNATIVE_TASK_FRAME, [ALTERNATIVE_TASK_LABEL])
gui.state('zoomed')
import random
def x(e):
	dc.create_feedback_original(random.randint(0,3))
gui.bind("<space>", x)
exp.run()