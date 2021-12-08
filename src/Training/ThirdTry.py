from Aliases import EventLog, Features
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractTrainableEntity import AbstractTrainableEntity
from TileEntities.Agent import Agent
from TileEntities.Monster import Monster
from TileEntities.SpikeTrap import SpikeTrap
from Training.Abstract import Abstract
from typing import cast
import math

class ThirdTry(Abstract):
	def __init__(self, gridWorld):
		super().__init__(gridWorld)
		self.exitMap = self.gridWorld.djikstraAdjacencyMap(self.gridWorld.exitPos, excludeNonTraversableEntities = True)

	def getFeatures(self, entity: AbstractTrainableEntity) -> Features:
		result = {}

		if isinstance(entity, Agent):
			dist = self.exitMap[entity.pos]['dist']
			result['dist_to_exit'] = 1 / (dist + 1)

			canAttack = False
			damageToTake = 0
			for tile, data in self.gridWorld.djikstraSearch(entity.pos, predicate = AbstractAggresiveEntity, excludeNonTraversableEntities = True, maxDistance = 4):
				for tileEntity in self.gridWorld.getEntitiesAtLocation(tile, AbstractAggresiveEntity):
					if tileEntity.team == entity.team:
						continue
					
					tileEntity = cast(AbstractAggresiveEntity, tileEntity)

					if isinstance(tileEntity, SpikeTrap):
						if data['dist'] == 0:
							damageToTake += tileEntity.attackDamage
					else:
						if data['dist'] == 1:
							canAttack = True
							if not isinstance(tileEntity, Monster) or tileEntity.cooldown <= 1:
								damageToTake += tileEntity.attackDamage

			result['will_die'] = 1 if entity.health <= damageToTake else 0
			# result['near_death'] = 1 if entity.health <= 15 else 0
			result['can_attack'] = 1 if canAttack else 0

		return result

	def evaluateReward(self, entity: AbstractTrainableEntity, eventLog: EventLog) -> float:
		score = 0

		if isinstance(entity, AbstractHitpointEntity) and entity.health == 0:
			score -= 100
		elif self.gridWorld.exitPos == entity.pos:
			score += 50

		for params in eventLog:
			match params['event']:
				case 'attack':
					score += 10 # Points just for attacking
					if params['target'].health == 0:
						score += 50 # Points for killing monster
				case 'health':
					score -= params['health'] / 5

		return score