from Aliases import Features
from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractPerceptionEntity import AbstractPerceptionEntity
from TileEntities.AbstractWeaponsEntity import AbstractWeaponEntity
from TileEntities.AbstractTrainableEntity import AbstractTrainableEntity
from Utils.Weights import Weights
from Utils.Cli import commandLineArgs

class Agent(AbstractMovableEntity, 
			AbstractHitpointEntity, 
			AbstractAggresiveEntity, 
			AbstractTrainableEntity,
			AbstractPerceptionEntity,
			AbstractWeaponEntity):

	team = 'agent'
	maxHitPoints = 100
	attackDamage = 10
	# action cost is how many turns it will take to do an action
	perceptionViewDistance = 3
	actionCost = 3
	weaponName = "default_weapon"
	weaponDamage = 10
	weaponDamageMultiplier = 2.0
	weaponReach = 1

	# set attack damage to do the weapon damage for now (so it simply replaces attack damage with weapon damage)
	#attackDamage = weaponDamage

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.discount = commandLineArgs.discount
		self.alpha  = commandLineArgs.alpha
		self.weights = Weights(randomize = True)

	def getAllActions(self):
		for tile in self.nearbyTiles:
			if self.gridWorld.isTileTraversable(tile):
				yield ('move', [tile])
			for tileItem in self.gridWorld.getTileData(tile):
				if isinstance(tileItem, AbstractHitpointEntity):
					yield ('attackEntity', [tileItem])

	def getBestAction(self):
		allActions = list(self.getAllActions())
		if len(allActions) == 0:
			return (None, 0)

		bestAction = None
		bestReward = None

		for action in allActions:
			features = self.simulateActionAndGetFeatures(action)
			predictedReward = self.calculatePredictedReward(features)
			
			if bestReward == None or predictedReward > bestReward:
				bestAction = action
				bestReward = predictedReward

		return (bestAction, bestReward)

	def learnFromExperience(self, priorFeatures: Features, reward: float):
		# print(priorFeatures, reward)
		_, bestReward = self.getBestAction()
		difference = (reward + self.discount * bestReward) - self.calculatePredictedReward(priorFeatures)
		for i in priorFeatures:
			self.weights[i] = self.weights[i] + self.alpha * difference * priorFeatures[i]

	def calculatePredictedReward(self, features: Features):
		return sum([features[i] * self.weights[i] for i in features])

	def tick(self):
		bestAction, _ = self.getBestAction()
		if bestAction != None:
			self.takeAction(bestAction)
