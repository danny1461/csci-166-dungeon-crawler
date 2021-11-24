from abc import ABC, abstractmethod

class Abstract(ABC):
	nextId = 1

	traversable = True
	team = 'gaia'

	def __init__(self, gridWorld):
		self.id = Abstract.nextId
		Abstract.nextId += 1

		self.gridWorld = gridWorld

	def __hash__(self):
		return self.id

	def __eq__(self, other):
		if isinstance(other, Abstract):
			return self.id == other.id
		return self.id == other

	@property
	def pos(self):
		return self.gridWorld.getTileEntityLocation(self)

	@property
	def x(self):
		return self.gridWorld.getTileEntityLocation(self)[0]

	@property
	def y(self):
		self.gridWorld.getTileEntityLocation(self)[1]

	def move(self, newX, newY):
		self.gridWorld.moveTileEntity(self, newX, newY)

	@abstractmethod
	def tick(self):
		pass

	def log(self, *args):
		self.gridWorld.log(*args)