from TileEntities.Abstract import Abstract as AbstractTileEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.Agent import Agent
from TileEntities.Human import Human
from TileEntities.Monster import Monster
from TileEntities.SpikeTrap import SpikeTrap
from random import random
from Aliases.Tile import Tile

class GridWorld:
	transitionDirections = [(1, 0), (0, 1), (-1, 0), (0, -1)]
	tileEntityMap = {
		'A': Agent,
		'H': Human,
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

	def getEntities(self):
		return self.entities

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

	# check if a tile is in a tuple/set of tiles
	def isTileInSetOfTiles(self, setOfTiles: Tile, check: Tile):
		for tile in setOfTiles:
			if(tile == check):
				return True
		
		return False

	# can we trace from a tile to another tile directly in a B-line (straight to the point)
	def isTileBlineTraceable(self, fromPos: Tile, toPos: Tile):
		traceable = True # default assumes we can look at starting tile, so we can see ourselves 
		tracer = fromPos
		initial = True   # initial trace is not checked for traverseability since the trace will bump into it's own starting position
		while (tracer != toPos):
			pastTracer = tracer
			
			xDiff = toPos[0] - tracer[0]
			yDiff = toPos[1] - tracer[1]
			
			if abs(xDiff) >= abs(yDiff):
				unit = xDiff / abs(xDiff)
				tracer = ( (int(tracer[0] + unit), tracer[1]) )
			
			else:
				unit = yDiff / abs(yDiff)
				tracer = ( (tracer[0], int(tracer[1] + unit)) )
				
			if (self.isTileTraversable(pastTracer) or initial):
				initial = False
				traceable = True
				
			else:
				traceable = False
				break

		#print("Tracer ", tracer, traceable)
		return traceable

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
			return False

		if not self.isTileTraversable(pos):
			return False

		self.map[entity.pos].remove(entity)
		self.entities[entity] = pos
		self.map[entity.pos].append(entity)

		return True

	def log(self, *args):
		if self.logging:
			print(*args)

	# get current turn of world
	def getTurn(self):
		return int(self.ticks/len(self.entities)) + 1

	# return a random percent
	def getRandomPercent(self):
		return random()

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