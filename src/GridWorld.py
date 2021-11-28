from TileEntities.Abstract import Abstract as AbstractTileEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.Agent import Agent
from TileEntities.Monster import Monster
from TileEntities.SpikeTrap import SpikeTrap
from Aliases import Tile
from Utils.PriorityQueue import PriorityQueue

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
		self.exitPos = None
		self.trackingActions = False

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

				if c == 'E':
					self.exitPos = loc

			if y >= self.height:
				self.height = y + 1

			x += 1

	def getEntityById(self, entityId):
		pos = self.getTileEntityLocation(entityId)
		for tileItem in self.getEntitiesAtLocation(pos):
			if tileItem.id == entityId:
				return tileItem

	def isValidTile(self, pos: Tile):
		if pos[0] < 0 or pos[0] >= self.width:
			return False
		if pos[1] < 0 or pos[1] >= self.height:
			return False

		return True

	def isTileTraversable(self, pos: Tile, excludeNonTraversableEntities = False):
		if not self.isValidTile(pos):
			return False

		for tileData in self.map[pos]:
			if isinstance(tileData, AbstractTileEntity):
				if not excludeNonTraversableEntities and not tileData.traversable:
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

	def getNearbyTraversableTiles(self, pos: Tile, excludeNonTraversableEntities = False):
		for tile in self.getNearbyTiles(pos):
			if not self.isTileTraversable(tile, excludeNonTraversableEntities):
				continue

			yield tile

	def djikstraSearch(self,
		pos: Tile,
		traversableOnly = True,
		excludeNonTraversableEntities = False,
		predicate = None,
		takeCount = None,
		maxDistance = None
	):
		"""
			In a graph where the edges are varying distances, this wouldn't be efficient.
			But we should be able to get away with it here
		"""
		if isinstance(predicate, type):
			cls = predicate
			predicate = lambda tile: any([isinstance(tileItem, cls) for tileItem in self.getTileData(tile)])

		fringe = PriorityQueue()
		fringe.update(pos, 0)
		visited = {}

		while len(fringe):
			tile, dist = fringe.popWithPriority()
			if maxDistance != None and dist > maxDistance:
				return

			visited[tile] = True
			if predicate == None or predicate(tile):
				yield (tile, dist)
				if takeCount != None:
					takeCount -= 1
					if takeCount == 0:
						return

			if traversableOnly:
				nearbyTiles = self.getNearbyTraversableTiles(tile, excludeNonTraversableEntities)
			else:
				nearbyTiles = self.getNearbyTiles(tile)

			dist += 1
			for nextTile in nearbyTiles:
				if nextTile not in visited:
					fringe.update(nextTile, dist)

	def getTileData(self, pos: Tile):
		if not self.isValidTile(pos):
			return []

		return self.map[pos]

	def getEntitiesAtLocation(self, pos: Tile):
		for tileItem in self.getTileData(pos):
			if isinstance(tileItem, AbstractTileEntity):
				yield tileItem

	def getTileEntityLocation(self, entity):
		if entity not in self.entities:
			return (None, None)

		return self.entities[entity]

	def moveTileEntity(self, entity, pos: Tile):
		if entity not in self.entities:
			return False

		if not self.isTileTraversable(pos):
			return False

		if self.isTrackingActions:
			oldPos = self.entities[entity]
			self.trackUndoAction(lambda: self.moveTileEntity(entity, oldPos))

		self.map[entity.pos].remove(entity)
		self.entities[entity] = pos
		self.map[entity.pos].append(entity)

		return True

	def log(self, *args):
		if not self.isTrackingActions and self.logging:
			print(*args)

	def trackActions(self):
		self.trackingActions = True
		self.events = []

	def stopTracking(self):
		self.trackingActions = False
		self.events = []

	def trackUndoAction(self, undoFn):
		self.events.append(undoFn)

	@property
	def isTrackingActions(self):
		return self.trackingActions

	def rollbackActions(self):
		self.trackingActions = False
		while len(self.events) > 0:
			fn = self.events.pop()
			fn()

	def tick(self):
		self.ticks += 1

		teamNdx = 0
		while teamNdx < len(self.teams):
			self.currentTeam = self.teamList[teamNdx]
			self.log("{}'s turn".format(self.currentTeam))
			toRemove = []

			for entity in self.teams[self.currentTeam]:
				if isinstance(entity, AbstractHitpointEntity) and entity.isDead:
					self.log('Entity {} at {},{} died'.format(entity.__class__.__name__, entity.x, entity.y))
					toRemove.append(entity)
					continue

				entity.tick()

				if isinstance(entity, Agent) and entity.pos == self.exitPos:
					self.log('Agent successfully exited the dungeon')
					toRemove.append(entity)

			for entity in toRemove:
				self.teams[self.currentTeam].remove(entity)
				self.map[entity.pos].remove(entity)
				self.entities.pop(entity)

			if len(self.teams[self.currentTeam]) == 0:
				self.teamList.remove(self.currentTeam)
				teamNdx -= 1