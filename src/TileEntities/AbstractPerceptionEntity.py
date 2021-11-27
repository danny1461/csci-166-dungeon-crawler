from TileEntities.Abstract import Abstract
from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from Aliases.Tile import Tile

class AbstractPerceptionEntity(Abstract):
	saw = False
	viewDistance = 5
	losBlocked = False

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.distance = type(self).viewDistance

	# is line of sight blocked (there is a wall/entity/object in the way)
	def isLineOfSightBlocked(self, toPos: Tile):
		tracer = self.pos
		print(self.pos, toPos)

		if (tracer != toPos):
			xDiff = toPos[0] - tracer[0]
			yDiff = toPos[1] - tracer[1]
			
			if abs(xDiff) >= abs(yDiff):
				unit = xDiff / abs(xDiff)
				self.move( (int(tracer[0] + unit), tracer[1]) )
			
			else:
				unit = yDiff / abs(yDiff)
				self.move( (tracer[0], int(tracer[1] + unit)) )
				
		while not(tracer == toPos):
			# move agent towards a tile in the dungeon
			if not(self.isTraverseable(tracer)):
				print("los blocked <------------")
				self.losBlocked = True
				break
			else:
				self.losBlocked = False

	# if our entity can see another entity (at position) of some kind
	def eyes(self, toPos: Tile, distance: int):
		if (self.isInRange(self.pos, toPos, distance)):
			self.saw = True
		else:
			self.saw = False


	@property
	def didSee(self):
		return self.saw