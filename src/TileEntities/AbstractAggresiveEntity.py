from TileEntities.Abstract import Abstract
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from Aliases import Tile

class AbstractAggresiveEntity(Abstract):
	attackDamage = 1

	def attackEntity(self, entity: AbstractHitpointEntity):
		self.triggerEvent('attack', target = entity)
		entity.damage(self.attackDamage)

	def attackTile(self, pos: Tile):
		for tileItem in self.gridWorld.getTileData(pos):
			if isinstance(tileItem, AbstractHitpointEntity):
				self.attackEntity(tileItem)