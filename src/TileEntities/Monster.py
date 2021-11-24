from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.Agent import Agent
from random import choice

class Monster(AbstractMovableEntity, AbstractHitpointEntity, AbstractAggresiveEntity):
	team = 'monster'
	maxHitPoints = 50
	attackDamage = 5

	def tick(self):
		self.log('Monster does nothing')