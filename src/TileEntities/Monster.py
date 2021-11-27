from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractActionEntity import AbstractActionEntity
from TileEntities.Agent import Agent
from random import choice

class Monster(AbstractMovableEntity, AbstractHitpointEntity, AbstractAggresiveEntity, AbstractActionEntity):
	team = 'monster'
	maxHitPoints = 50
	attackDamage = 5
	actionCost = 2

	def tick(self):
		self.log('Monster does nothing')