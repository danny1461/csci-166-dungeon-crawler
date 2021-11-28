from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractActionEntity import AbstractActionEntity
from TileEntities.AbstractPerceptionEntity import AbstractPerceptionEntity
from TileEntities.AbstractWeaponsEntity import AbstractWeaponEntity
from TileEntities.AbstractPointsClass import AbstractPointsEntity

class Agent(AbstractMovableEntity, 
			AbstractHitpointEntity, 
			AbstractAggresiveEntity, 
			AbstractActionEntity, 
			AbstractPerceptionEntity, 
			AbstractWeaponEntity, 
			AbstractPointsEntity):

	team = 'agent'
	maxHitPoints = 100
	attackDamage = 10
	pointsTotal = 0
	# action cost is how many turns it will take to do an action
	perceptionViewDistance = 10
	actionCost = 3
	weaponName = "default_weapon"
	weaponDamage = 10
	weaponDamageMultiplier = 2.0
	weaponReach = 1

	attackDamage = weaponDamage

	direction = "left"

	def tick(self):
		self.log("Position: ", self.pos)
		#self.log(self.turn)
		#self.actionCounter(self.actionCost)
		#self.log(self.randomPercent)
		#self.actionChance(1)
		#self.log(self.chanceSuccessful)
		#self.eyes((2,2))
		#print("Did see the object: ", self.didSee)
		#self.hasLineOfSight((2,2))
		#print("Line of sight: ", self.los)
		#self.move((2,10))
		if(self.pos[0] == 1):
			self.direction = "right"
		self.moveDirection(self.direction)

		self.log(self.team, "end log")