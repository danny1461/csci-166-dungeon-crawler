from Aliases import EventLog, Features
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractTrainableEntity import AbstractTrainableEntity
from TileEntities.Agent import Agent
from TileEntities.Monster import Monster
from Training.Abstract import Abstract
import math

class FirstTry(Abstract):
	def getFeatures(self, entity: AbstractTrainableEntity) -> Features:
		result = {}

		if isinstance(entity, Agent):
			if self.gridWorld.exitPos == entity.pos:
				result['dist_to_exit'] = 1
			else:
				result['dist_to_exit'] = 1 / (abs(self.gridWorld.exitPos[0] - entity.pos[0]) + abs(self.gridWorld.exitPos[1] - entity.pos[1]))

		for monsterTile, monsterDist in self.gridWorld.djikstraSearch(entity.pos, predicate = Monster, maxDistance = 3, excludeNonTraversableEntities = True):
			result['can_get_hurt'] = 1 if monsterDist == 1 else 0
			result['dist_to_monster'] = 1 / monsterDist

			monster = [e for e in self.gridWorld.getEntitiesAtLocation(monsterTile) if isinstance(e, Monster)][0]
			hitsToKill = math.ceil(monster.health / entity.attackDamage)
			hitsToDie = math.ceil(entity.health / monster.attackDamage)
			result['can_win'] = 1 if hitsToKill < hitsToDie else 0
			break

		return result

	def evaluateReward(self, entity: AbstractTrainableEntity, eventLog: EventLog) -> float:
		score = 0

		if isinstance(entity, AbstractHitpointEntity) and entity.health == 0:
			score -= 100
		elif self.gridWorld.exitPos == entity.pos:
			score += 100

		for params in eventLog:
			match params['event']:
				case 'attack':
					if params['target'].health == 0:
						score += 50 # Points for killing monster
				case 'health':
					if params['health'] > 0: # points for healing only... getting hurt is not BAD per se
						score += params['health']

		return score