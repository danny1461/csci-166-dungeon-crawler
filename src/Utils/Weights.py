from random import uniform

class Weights(dict):
	def __init__(self, randomize = False):
		self.randomize = randomize

	def __getitem__(self, ndx):
		return self.setdefault(ndx, uniform(-0.1, 0.1) if self.randomize else 0)