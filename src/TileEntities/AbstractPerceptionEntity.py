from TileEntities.Abstract import Abstract
from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from Aliases.Tile import Tile

class AbstractPerceptionEntity(Abstract):
	saw = False
	viewDistance = 5
	los = True

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.distance = type(self).viewDistance

	# has a line of sight to whatever tile desired (there is a wall/entity/object in the way)
	def hasLineOfSight(self, toPos: Tile):
		self.los = self.isBlineTraceable(self.pos, toPos)

	# if our entity can see another entity (at tile position) of some kind given a distance
	def eyes(self, toPos: Tile, distance: int):
		if (self.isBlineTraceable(self.pos, toPos)):
			if (self.isInRange(self.pos, toPos, distance)):
				print("got here")
				self.saw = True
				
		else:
			self.saw = False

	@property
	def didSee(self):
		return self.saw