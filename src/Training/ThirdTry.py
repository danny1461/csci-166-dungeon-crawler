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
	def getFeatures(self, entity: AbstractTrainableEntity) -> Features:
		result = {}

		if isinstance(entity, Agent):
			exitPos, exitDist = list(self.gridWorld.djikstraSearch(entity.pos, excludeNonTraversableEntities = True, predicate = lambda tile: self.gridWorld.map[tile][0] == 'E'))[0]
			result['dist_to_exit'] = 1 / (exitDist + 1)

			canAttack = False
			damageToTake = 0
			# monsterDistance = None
			for tile, dist in self.gridWorld.djikstraSearch(entity.pos, predicate = AbstractAggresiveEntity, excludeNonTraversableEntities = True, maxDistance = 4):
				for tileEntity in self.gridWorld.getEntitiesAtLocation(tile, AbstractAggresiveEntity):
					if tileEntity == entity:
						continue
					
					tileEntity = cast(AbstractAggresiveEntity, tileEntity)

					if isinstance(tileEntity, SpikeTrap):
						if dist == 0:
							damageToTake += tileEntity.attackDamage
					else:
						# if monsterDistance == None or dist < monsterDistance:
						# 	monsterDistance = dist
						if dist == 1:
							damageToTake += tileEntity.attackDamage
							canAttack = True

			# result['will_get_hurt'] = min(damageToTake, 1)
			# if monsterDistance != None:
			# 	result['dist_to_monster'] = 1 / monsterDistance
			result['will_die'] = 1 if entity.health <= damageToTake else 0
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