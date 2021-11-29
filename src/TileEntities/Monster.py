from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractActionEntity import AbstractActionEntity
from TileEntities.AbstractPerceptionEntity import AbstractPerceptionEntity
from TileEntities.AbstractWeaponsEntity import AbstractWeaponEntity
from TileEntities.AbstractPointsEntity import AbstractPointsEntity
from TileEntities.AbstractInteractionMethods import AbstractInteractionMethods
from TileEntities.Agent import Agent
from random import choice

class Monster(AbstractMovableEntity, 
			AbstractHitpointEntity, 
			AbstractAggresiveEntity, 
			AbstractActionEntity, 
			AbstractPerceptionEntity, 
			AbstractWeaponEntity, 
			AbstractPointsEntity):

	team = 'monster'
	maxHitPoints = 100
	attackDamage = 10
	# action cost is how many turns it will take to do an action
	perceptionViewDistance = 3
	actionCost = 2
	weaponName = "claws"
	weaponDamage = 20
	weaponDamageMultiplier = 2.0
	weaponReach = 1

	attackDamage = weaponDamage

	aim = AbstractInteractionMethods

	def __init__(self, *args, **kwargs):
		self.aim.interactionPossible.append(self)
		super().__init__(*args, **kwargs)

	def tick(self):
		self.aim.checkPossibleInteractions(self)
		self.aim.fight(self)
		self.log('Monster end log')