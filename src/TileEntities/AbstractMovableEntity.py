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
			nextPos = (int(mePos[0] + unit), mePos[1])
			if self.gridWorld.isTileTraversable(nextPos):
				self.move( nextPos )
				return
				
		if yDiff != 0:
			unit = yDiff / abs(yDiff)
			nextPos = (mePos[0], int(mePos[1] + unit))
			if self.gridWorld.isTileTraversable(nextPos):
				self.move( nextPos )