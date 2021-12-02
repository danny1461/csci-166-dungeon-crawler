from abc import ABC, abstractmethod
from GridWorld import GridWorld

class Abstract(ABC):
	def __init__(self, world: GridWorld):
		self.gridWorld = world

	@abstractmethod
	def render(self):
		pass