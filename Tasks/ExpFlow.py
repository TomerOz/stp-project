import ipdb

class Flow(object):
		def __init__(self):
			self.current_index = 0
			self.tasks_lambdas_list = [] # should be filled by "add_tasks"
		
		def add_tasks(self, tasks_lambdas_list):
			self.tasks_lambdas_list = tasks_lambdas_list
				
		def next(self, start_event=None):
			if self.current_index < len(self.tasks_lambdas_list):
				print("Flow continues")
				self.tasks_lambdas_list[self.current_index]()
				self.current_index += 1
			else:
				print("The End")