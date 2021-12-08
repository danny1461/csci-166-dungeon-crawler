from TileEntities.Abstract import Abstract
from Aliases import Tile

class AbstractMovableEntity(Abstract):
	@property
	def nearbyTraversableTiles(self):
		return self.gridWorld.getNearbyTraversableTiles(self.gridWorld.getTileEntityLocation(self))

	def move(self, pos: Tile):
		return self.gridWorld.moveTileEntity(self, pos)

	def moveTowards(self, pos: Tile):
		adjacencyMap = self.gridWorld.djikstraAdjacencyMap(pos, traversableFn = self.traverableFn(pos))

		if self.pos in adjacencyMap:
			return self.move(adjacencyMap[self.pos]['previous'])

		return False

	def traverableFn(self, target):
		def fn(foundTile):
			if foundTile == target or foundTile == self.pos:
				return True
			return self.gridWorld.isTileTraversable(foundTile)
		
		return fn

	def predicateFn(self, target):
		def fn(foundTile):
			return foundTile == target

		return fn