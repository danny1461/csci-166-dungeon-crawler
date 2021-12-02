from TileEntities.Abstract import Abstract
from Aliases import Tile

class AbstractPerceptionEntity(Abstract):
	saw = False
	perceptionViewDistance = 5
	los = False

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.distance = type(self).perceptionViewDistance

	# has a line of sight to whatever tile desired (there is a wall/entity/object in the way)
	def setLineOfSight(self, toPos: Tile):
		self.los = self.isBlineTraceable(self.pos, toPos)

	# if our entity can see another entity (at tile position) of some kind given a distance
	def setEyes(self, toPos: Tile):
		if (self.isBlineTraceable(self.pos, toPos)):
			if (self.isInRange(self.pos, toPos, self.distance)):
				self.saw = True
			else:
				self.saw = False
		else:
			self.saw = False

	@property
	def hasLos(self):
		return self.los

	@property
	def canSee(self):
		return self.saw