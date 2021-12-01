from TileEntities.Abstract import Abstract
from Aliases import Tile

class AbstractMovableEntity(Abstract):
	@property
	def nearbyTraversableTiles(self):
		return self.gridWorld.getNearbyTraversableTiles(self.gridWorld.getTileEntityLocation(self))

	def move(self, pos: Tile):
		return self.gridWorld.moveTileEntity(self, pos)

	def moveTowards(self, pos: Tile):
		# This is really bad code, but still better than before
		bestTile = None
		bestDist = float('inf')
		for tile in self.gridWorld.getNearbyTiles(self.pos):
			if self.gridWorld.isTileTraversable(tile):
				for _, dist in self.gridWorld.djikstraSearch(tile, traversableFn = self.traverableFn(pos), predicate = self.predicateFn(pos)):
					if dist < bestDist:
						bestTile = tile
						bestDist = dist
						break

		if bestTile != None:
			return self.move(bestTile)
		
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