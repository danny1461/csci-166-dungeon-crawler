from TileEntities.Abstract import Abstract
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from Aliases.Tile import Tile

class AbstractAggresiveEntity(Abstract):
	attackDamage = 1

	def attackEntity(self, entity: AbstractHitpointEntity):
		entity.damage(type(self).attackDamage)

	def attackTile(self, pos: Tile):
		for tileItem in self.gridWorld.getTileData(pos):
			if isinstance(tileItem, AbstractHitpointEntity):
				tileItem.damage(type(self).attackDamage)