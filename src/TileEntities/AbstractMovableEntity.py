from TileEntities.Abstract import Abstract
from Aliases import Tile

class AbstractMovableEntity(Abstract):
	@property
	def nearbyTraversableTiles(self):
		return self.gridWorld.getNearbyTraversableTiles(self.gridWorld.getTileEntityLocation(self))

	def move(self, pos: Tile):
		self.gridWorld.moveTileEntity(self, pos)

	def moveTowards(self, pos: Tile):
		mePos = self.pos
		xDiff = pos[0] - mePos[0]
		yDiff = pos[1] - mePos[1]

		if abs(xDiff) >= abs(yDiff):
			unit = xDiff / abs(xDiff)
			self.move( (int(mePos[0] + unit), mePos[1]) )
		else:
			unit = yDiff / abs(yDiff)
			self.move( (mePos[0], int(mePos[1] + unit)) )