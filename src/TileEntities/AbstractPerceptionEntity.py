from TileEntities.Abstract import Abstract
from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from Aliases.Tile import Tile

class AbstractPerceptionEntity(Abstract):
	saw = False
	viewDistance = 5
	losBlocked = False
	tracerPos = (0,0)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.distance = type(self).viewDistance
		self.tracer = self.tracerPos

	# is line of sight blocked (there is a wall/entity/object in the way)
	def isLineOfSightBlocked(self, toPos: Tile):
		self.tracer = self.pos
		while (self.tracer != toPos):
			xDiff = toPos[0] - self.tracer[0]
			yDiff = toPos[1] - self.tracer[1]
			
			if abs(xDiff) >= abs(yDiff):
				unit = xDiff / abs(xDiff)
				self.tracer = ( (int(self.tracer[0] + unit), self.tracer[1]) )
			
			else:
				unit = yDiff / abs(yDiff)
				self.tracer = ( (self.tracer[0], int(self.tracer[1] + unit)) )
				
			# move agent towards a tile in the dungeon
			if not(self.isTraverseable(self.tracer)):
				self.losBlocked = True
				break
			else:
				self.losBlocked = False

	# bugged right now, will fix later tonight
	# if our entity can see another entity (at tile position) of some kind given a distance
	def eyes(self, toPos: Tile, distance: int):
		if not(self.isLineOfSightBlocked(toPos)):
			if (self.isInRange(self.pos, toPos, distance)):
				self.saw = True
			else:
				self.saw = False
		else:
			self.saw = False

	@property
	def didSee(self):
		return self.saw