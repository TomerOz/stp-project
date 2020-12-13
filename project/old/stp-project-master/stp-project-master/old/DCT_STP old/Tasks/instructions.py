import os


BACKGROUND = "black"
FOREGROUND = "white"


class Instructions(object):
	def __init__(self, dct_task, gui, exp, flow, imagepath):
		self.current_pic = 0
		self.dct_task = dct_task
		self.exp = exp
		self.gui = gui
		self.flow = flow
		self.imagepath = imagepath
		self.instruction_pics = os.listdir(self.imagepath)
		
	def start_instrunctions(self):
		self.gui.bind("<space>", self.next_pic)
		self.exp.create_frame("instructions_f", 
				full_screen=True,
				background_color=BACKGROUND)
				
		img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
		self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
		
		self.exp.display_frame("instructions_f", ["instructions_l"])
		
	def next_pic(self, eff):
		self.current_pic+=1
		if self.current_pic < len(self.instruction_pics):
			img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
			self.exp.LABELS_BY_FRAMES["instructions_f"]["instructions_l"].destroy()
			self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
			self.exp.display_frame("instructions_f", ["instructions_l"])
		else:
			self.flow.flag = True
	
	def inst_flow(self):
		self.start_instrunctions()
		self.gui.bind("<space>", self.next_pic)
			