
CALLBACK_WAIT_TIME = 500

class Flow(object):
		def __init__(self, gui):
			self.flag = False # controling the execution of the function to be called
			self.gui = gui
		
		def callback(self, fanc_to_call, *args):
			if self.flag:
				fanc_to_call(*args)
				self.flag = False
			else:
				self.gui.after(CALLBACK_WAIT_TIME, lambda:self.callback(fanc_to_call, *args))
	
		def start_exp(self, eff):	# eff is just the irelevant event passed with the binding
			''' This is the exprimental flow defacto.
					Any new task or unrealted windo should appear here.
					Tomer - consider integrating this class inside ExpGui'''
			
			self.gui.unbind("<Right>")	
			menu.show()
			self.callback(instructions.inst_flow)
			self.callback(task.start_task)

		def second_task(self, event=None):
			self.flag = True
			self.gui.unbind("<Right>")
			self.gui.unbind("<Left>")
			self.callback(instructions2.inst_flow)
			self.callback(task2.start_task)
