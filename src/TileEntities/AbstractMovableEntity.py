from TileEntities.Abstract import Abstract
from Aliases import Tile

class AbstractMovableEntity(Abstract):
	@property
	def nearbyTraversableTiles(self):
		return self.gridWorld.getNearbyTraversableTiles(self.gridWorld.getTileEntityLocation(self))

	# move agent directly to the said tile position (like a teleporter)
	def move(self, pos: Tile):
		self.gridWorld.moveTileEntity(self, pos)

	# move agent in a direction towards a certain tile (cardinal (compass) directions or transversal (up, down, left, right))
	def moveDirection(self, dir: str):
		horz = 0
		vert = 0
		meDir = dir.lower()
		if meDir in ('north', 'up'):
			vert = -1
		if meDir in ('south', 'down'):
			vert = 1
		if meDir in ('east', 'left'):
			horz = -1
		if meDir in ('west', 'right'):
			horz = 1
		self.move((self.x + (horz), self.y + (vert)))

	# move agent towards a tile in the dungeon
	def moveTowards(self, pos: Tile):
		mePos = self.pos
		if(mePos != pos):
			xDiff = pos[0] - mePos[0]
			yDiff = pos[1] - mePos[1]

			if abs(xDiff) >= abs(yDiff):
				unit = xDiff / abs(xDiff)
				self.move( (int(mePos[0] + unit), mePos[1]) )
			else:
				unit = yDiff / abs(yDiff)
				self.move( (mePos[0], int(mePos[1] + unit)) )