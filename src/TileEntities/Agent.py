from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity

class Agent(AbstractMovableEntity, AbstractHitpointEntity, AbstractAggresiveEntity):
	team = 'agent'
	maxHitPoints = 100
	attackDamage = 10

	def tick(self):
		#self.log(self.pos)
		#self.log(self.turn)
		self.log('Agent does nothing')

	