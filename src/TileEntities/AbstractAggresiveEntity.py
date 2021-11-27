from TileEntities.Abstract import Abstract
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from Aliases.Tile import Tile

class AbstractAggresiveEntity(Abstract):
	attackDamage = 1

	# for directly attacking an entity (can be a player or non-player)
	def attackEntity(self, entity: AbstractHitpointEntity):
		entity.damage(type(self).attackDamage)

	# for attacking anything on a specific tile (implies splash damage-esque attack)
	def attackTile(self, pos: Tile):
		for tileItem in self.gridWorld.getTileData(pos):
			if isinstance(tileItem, AbstractHitpointEntity):
				tileItem.damage(type(self).attackDamage)