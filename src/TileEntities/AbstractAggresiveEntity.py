from TileEntities.Abstract import Abstract
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from Aliases import Tile

class AbstractAggresiveEntity(Abstract):
	attackDamage = 1

	# for directly attacking an entity (can be a player or non-player)
	def attackEntity(self, entity: AbstractHitpointEntity):
		self.triggerEvent('attack', target = entity)
		entity.damage(self.attackDamage)

	# for attacking anything on a specific tile (implies splash damage-esque attack)
	def attackTile(self, pos: Tile):
		for tileItem in self.gridWorld.getTileData(pos):
			if isinstance(tileItem, AbstractHitpointEntity):
				self.attackEntity(tileItem)