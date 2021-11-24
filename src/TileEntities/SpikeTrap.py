from .Abstract import Abstract
from .AbstractHitpointEntity import AbstractHitpointEntity

class SpikeTrap(Abstract):
	damage = 5

	def tick(self):
		for entity in self.gridWorld.getTileData(self.x, self.y):
			if isinstance(entity, AbstractHitpointEntity):
				entity.damage(SpikeTrap.damage)