from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractActionEntity import AbstractActionEntity
from TileEntities.AbstractPerceptionEntity import AbstractPerceptionEntity
from TileEntities.AbstractWeaponsEntity import AbstractWeaponEntity
from TileEntities.AbstractPointsClass import AbstractPointsEntity
from TileEntities.AbstractInteractionClass import AbstractInteractionEntity
from TileEntities.Agent import Agent
from random import choice

class Monster(AbstractMovableEntity, 
			AbstractHitpointEntity, 
			AbstractAggresiveEntity, 
			AbstractActionEntity, 
			AbstractPerceptionEntity, 
			AbstractWeaponEntity, 
			AbstractPointsEntity,
			AbstractInteractionEntity):

	team = 'monster'
	maxHitPoints = 100
	attackDamage = 10
	# action cost is how many turns it will take to do an action
	viewDistance = 3
	actionCost = 2
	weaponName = "claws"
	weaponDamage = 20
	weaponDamageMultiplier = 2.0
	weaponReach = 1

	def __init__(self, *args, **kwargs):
		self.interactionPossible.append(self)
		super().__init__(*args, **kwargs)
		self.attackDamage = self.weaponDamage

	def tick(self):
		self.log('Monster does nothing')