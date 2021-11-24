from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity

class SpikeTrap(AbstractAggresiveEntity):
	attackDamage = 5

	def tick(self):
		self.attackTile(self.pos)