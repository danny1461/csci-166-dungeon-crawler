from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractActionEntity import AbstractActionEntity
from TileEntities.AbstractPerceptionEntity import AbstractPerceptionEntity
from TileEntities.AbstractWeaponsEntity import AbstractWeaponEntity
from TileEntities.Agent import Agent
from random import choice

class Monster(AbstractMovableEntity, 
			AbstractHitpointEntity, 
			AbstractAggresiveEntity, 
			AbstractActionEntity, 
			AbstractPerceptionEntity, 
			AbstractWeaponEntity):

	team = 'monster'
	maxHitPoints = 50
	attackDamage = 5
	# action cost is how many turns it will take to do an action
	perceptionViewDistance = 3
	actionCost = 2
	weaponName = "claws"
	weaponDamage = 20
	weaponDamageMultiplier = 2.0
	weaponReach = 1

	#attackDamage = weaponDamage

	def tick(self):
		# Is an agent right next to us?
		agentTile = self.searchTileFirst(self.nearbyTiles, Agent)
		if agentTile != None:
			self.log('Monster attacks agent at:', agentTile)
			self.attackTile(agentTile)
			return

		# Can we find an agent within 3 blocks?
		for agentTile, agentDist in self.gridWorld.djikstraSearch(self.pos, maxDistance = 3, predicate = Agent, excludeNonTraversableEntities = True):
			self.log('Monster moves towards agent at:', agentTile)
			self.moveTowards(agentTile)
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
