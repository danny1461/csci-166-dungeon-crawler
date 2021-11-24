from .TileEntities.Abstract import Abstract as AbstractTileEntity
from .TileEntities.Monster import Monster
from .TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from .TileEntities.SpikeTrap import SpikeTrap
from .TileEntities.Agent import Agent

class GridWorld:
	transitionDirections = [(1, 0), (0, 1), (-1, 0), (0, -1)]
	tileEntityMap = {
		'M': Monster,
		'S': SpikeTrap,
		'A': Agent
	}

	def __init__(self, fromFile = None, fromString = None, logging = False):
		self.logging = logging
		self.tick = -1

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
		self.entities = {}
		self.teams = {}
		self.teamList = []
		length = len(mapString)
		while cursor < length:
			c = mapString[cursor]
			cursor += 1

			if c == "\n":
				self.width = x
				x = 0
				y += 1
				continue

			loc = (x, y)

			if c in GridWorld.tileEntityMap:
				tileClass = GridWorld.tileEntityMap[c]
				tileInst = tileClass(self, location = loc)
				self.map[loc] = [' ', tileInst]
				self.entities[tileInst] = (x, y)

				if tileInst.team not in self.teams:
					self.teams[tileInst.team] = []
					self.teamList.append(tileInst.team)
				self.teams[tileInst.team].append(tileInst)
			else:
				self.map[loc] = [c]

			if y >= self.height:
				self.height = y + 1

			x += 1

	def isValidTile(self, x, y):
		if x < 0 or x >= self.width:
			return False
		if y < 0 or y >= self.height:
			return False

		return True

	def isTileTraversable(self, x, y):
		if not self.isValidTile(x, y):
			return False

		for tileData in self.map[(x, y)]:
			if isinstance(tileData, AbstractTileEntity):
				if not tileData.traversable:
					return False
			elif tileData == 'W':
				return False

		return True

	def getTraversableTiles(self, x, y):
		result = []
		for dx, dy in GridWorld.transitionDirections:
			nx = x + dx
			ny = y + dy
			
			if not self.isTileTraversable(nx, ny):
				continue

			result.append( (nx, ny) )
		
		return result

	def getTilesWithinManhatenDistance(self, x, y, distance):
		if distance == 0:
			return [(x, y)]

		result = []
		dir = 1
		x -= distance
		for i in range(2 * distance + 1):
			if self.isValidTile(x, y):
				result.append((x, y))
			
			for j in range(distance if dir == 1 else distance - 1):
				x += 1 * dir
				y += -1 * dir
				if self.isValidTile(x, y):
					result.append((x, y))
			y += 1
			dir *= -1

		return result

	def getTileData(self, x, y):
		if not self.isValidTile(x, y):
			return []

		return self.map[(x, y)]

	def getTileEntityLocation(self, entity):
		if entity not in self.entities:
			return (None, None)

		return self.entities[entity]

	def moveTileEntity(self, entity, x, y):
		if entity not in self.entities:
			return

		self.entities[entity] = (x, y)

	def log(self, *args):
		if self.logging:
			print(*args)

	def tick(self):
		self.tick += 1
		if len(self.teamList):
			team = self.teamList[self.tick % len(self.teamList)]
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
				self.entities.pop(entity)