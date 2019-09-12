MAIN_FRAME = 'afact_frame'
FEEDBACK_LABEL = 'feedback_label'


class AfactGui(object):
	
	def __init__(self, gui, exp, width=200, height=400):
		self.gui = gui
		self.exp = exp
		self.width = width
		self.height = height
		self.feedback_canvas = None # Will be later created
		self.ammount_of_ticks = 10
		
	def create_feedback_canvas(self):
		'''creates the template background of the feedback object'''
		
		self.exp.create_frame(MAIN_FRAME)
		self.exp.create_label(FEEDBACK_LABEL, MAIN_FRAME)
		feedback_label_ref = self.exp.LABELS_BY_FRAMES[MAIN_FRAME][FEEDBACK_LABEL]
		
		self.feedback_canvas = self.exp.tk.Canvas(feedback_label_ref, width=self.width, height=self.height)
		
		tick_area = self.height*0.8333333333333334
		top_space = int((self.height - tick_area)/2)
		bottom_space = tick_area + top_space

		tick_space = int(tick_area/self.ammount_of_ticks)
		tick_middle = int(self.height/2) # inorder ti nake it 0 to 100
		all_ticks = range(self.ammount_of_ticks) + [self.ammount_of_ticks] # including zero and max
		
		for i,t in enumerate(all_ticks):
			tick = (t*tick_space) + top_space
			tick_text = int((self.ammount_of_ticks**2)/2) - i*self.ammount_of_ticks 
			#tick_text = str(tick)
			
			self.feedback_canvas.create_line(35, tick, 42, tick)
			self.feedback_canvas.create_text(20,tick,  text=tick_text, font="David 14") 
			print tick
		
		self.feedback_canvas.create_line(42,top_space, 42, bottom_space)
		
		
		#self.canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
        #                text="Click the bubbles that are multiples of two.")
		
		
		self.feedback_canvas.create_rectangle(68, tick_middle, 168, top_space-10, fill="green")
		self.feedback_canvas.pack()
		
	def create_feedback(self):
		pass
	
	def show_feedback(self):
		pass
		
class AfactTask(object):
	def __init__(self):
		pass


def main():
	
	from ExGui import Experiment
	
	exp = Experiment()
	gui = exp.gui
	
	afact_gui = AfactGui(gui, exp)
	afact_gui.create_feedback_canvas()
	
	exp.display_frame(MAIN_FRAME, [FEEDBACK_LABEL])
	gui.state('zoomed')
	exp.run()
	
if __name__ == '__main__':
	main()