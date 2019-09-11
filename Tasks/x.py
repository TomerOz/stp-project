import ipdb
from x2 import SomeObject

class nothing(object):
	def __init__(self, some_object):
		self.some_object = some_object
		
	def init_some_object(self):
		self.some_object()
		print self.some_object.x
		
data_manager = SomeObject()
xnothing = nothing(data_manager)

ipdb.set_trace()
print data_manager.x
xnothing.init_some_object()
print data_manager.x
