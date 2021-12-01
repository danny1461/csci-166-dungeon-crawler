from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.Agent import Agent
from random import choice, randint

class Monster(AbstractMovableEntity, AbstractHitpointEntity, AbstractAggresiveEntity):
	team = 'monster'
	maxHitPoints = 50
	attackDamage = 5
	moveCooldownDefault = 2

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.health = randint(50, 300)
		self.moveCooldown = 0

	def tick(self):
		# Is an agent right next to us?
		agentTile = self.searchTileFirst(self.nearbyTiles, Agent)
		if agentTile != None:
			self.log('Monster attacks agent at:', agentTile)
			self.attackTile(agentTile)
			return

		self.moveCooldown -= 1
		if self.moveCooldown > 0:
			return
		self.moveCooldown = self.moveCooldownDefault

		# Can we find an agent within 3 blocks?
		for agentTile, agentDist in self.gridWorld.djikstraSearch(self.pos, maxDistance = 6, predicate = Agent, excludeNonTraversableEntities = True):
			self.log('Monster moves towards agent at:', agentTile)
			if self.moveTowards(agentTile):
				return

		# Move randomly but don't move onto a tile that will attack us
		options = []
		for tile in self.nearbyTraversableTiles:
			for tileItem in self.gridWorld.getTileData(tile):
				if isinstance(tileItem, AbstractAggresiveEntity):
					break
			else:
				options.append(tile)

		if len(options) > 0:
			nextTile = choice(options)
			self.log('Monster moves randomly to:', nextTile)
			self.move(nextTile)