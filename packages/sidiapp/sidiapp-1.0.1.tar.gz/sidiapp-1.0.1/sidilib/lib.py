




class SidiApp():

	def __init__(self, name='sidi-app', version='1.0.0'):
		self.name = name
		self.version = version

	def __str__(self):
		return '<SidiApp: name={:5s}, version={:s}>'.format(self.name, self.version)



def run():
	print(str(SidiApp()))


import sidilib


