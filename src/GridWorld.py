from TileEntities.Abstract import Abstract as AbstractTileEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.Agent import Agent
from TileEntities.Monster import Monster
from TileEntities.SpikeTrap import SpikeTrap
from Aliases.Tile import Tile

class GridWorld:
	transitionDirections = [(1, 0), (0, 1), (-1, 0), (0, -1)]
	tileEntityMap = {
		'A': Agent,
		'M': Monster,
		'S': SpikeTrap,
	}

	def __init__(self, fromFile = None, fromString = None, logging = False):
		self.logging = logging
		self.ticks = -1
		self.teamNdx = -1

		if fromFile != None:
			self.loadMapFile(fromFile)
		elif fromString != None:
			self.loadMapString(fromString)
	
	def loadMapFile(self, filePath):
		f = open(filePath, 'r')
		try:
			self.loadMapString(f.read())
		finally:
			f.close()

	def loadMapString(self, mapString):
		x = 0
		y = 0

		self.width = 0
		self.height = 0
		cursor = 0

		self.map = {}
		self.entities: dict[AbstractTileEntity, Tile] = {}
		self.teams: dict[str, list[AbstractTileEntity]] = {}
		self.teamList: list[str] = []
		length = len(mapString)
		while cursor < length:
			c = mapString[cursor]
			cursor += 1

			if c == "\n":
				self.width = x
				x = 0
				y += 1
				continue

			loc: Tile = (x, y)

			if c in GridWorld.tileEntityMap:
				tileClass = GridWorld.tileEntityMap[c]
				tileInst = tileClass(self)
				self.map[loc] = [' ', tileInst]
				self.entities[tileInst] = loc

				if tileInst.team not in self.teams:
					self.teams[tileInst.team] = []
					self.teamList.append(tileInst.team)
				self.teams[tileInst.team].append(tileInst)
			else:
				self.map[loc] = [c]

			if y >= self.height:
				self.height = y + 1

			x += 1

	def isValidTile(self, pos: Tile):
		if pos[0] < 0 or pos[0] >= self.width:
			return False
		if pos[1] < 0 or pos[1] >= self.height:
			return False

		return True

	def isTileTraversable(self, pos: Tile):
		if not self.isValidTile(pos):
			return False

		for tileData in self.map[pos]:
			if isinstance(tileData, AbstractTileEntity):
				if not tileData.traversable:
					return False
			elif tileData == 'W':
				return False

		return True

	def getNearbyTiles(self, pos: Tile):
		for dx, dy in GridWorld.transitionDirections:
			t = (pos[0] + dx, pos[1] + dy)
			
			if not self.isValidTile(t):
				continue

			yield t

	def getTraversableTiles(self, pos: Tile):
		for tile in self.getNearbyTiles(pos):
			if not self.isTileTraversable(tile):
				continue

			yield tile

	def getTilesWithinManhatenDistance(self, pos: Tile, distance: int):
		if distance == 0:
			return [pos]

		dir = 1
		x = pos[0] - distance
		y = pos[1]
		for i in range(2 * distance + 1):
			if self.isValidTile( (x, y) ):
				yield (x, y)
			
			for j in range(distance if dir == 1 else distance - 1):
				x += 1 * dir
				y += -1 * dir
				if self.isValidTile( (x, y) ):
					yield (x, y)
			y += 1
			dir *= -1

	def breadthFirstSearch(self, pos: Tile):
		fringe = [pos]
		visited = {pos: True}

		while len(fringe):
			tile = fringe.pop(0)
			yield tile

			for nextTile in self.getTraversableTiles(tile):
				if nextTile not in visited:
					fringe.append(nextTile)
					visited[nextTile] = True

	def getTileData(self, pos: Tile):
		if not self.isValidTile(pos):
			return []

		return self.map[pos]

	def getTileEntityLocation(self, entity):
		if entity not in self.entities:
			return (None, None)

		return self.entities[entity]

	def moveTileEntity(self, entity, pos: Tile):
		if entity not in self.entities:
			return

		self.map[entity.pos].remove(entity)
		self.entities[entity] = pos
		self.map[entity.pos].append(entity)

	def log(self, *args):
		if self.logging:
			print(*args)

	def tick(self):
		self.ticks += 1

		if len(self.teamList):
			self.teamNdx += 1
			if self.teamNdx >= len(self.teamList):
				self.teamNdx -= len(self.teamList)

			team = self.teamList[self.teamNdx]
			self.log("{}'s turn".format(team))
			toRemove = []
			for entity in self.teams[team]:
				if isinstance(entity, AbstractHitpointEntity) and entity.isDead:
					self.log('Entity {} at {},{} died'.format(entity.__class__.__name__, entity.x, entity.y))
					toRemove.append(entity)
					continue

				entity.tick()

			for entity in toRemove:
				self.teams[team].remove(entity)
				self.map[entity.pos].remove(entity)
				self.entities.pop(entity)

			if len(self.teams[team]) == 0:
				self.teamList.remove(team)
				self.teamNdx -= 1