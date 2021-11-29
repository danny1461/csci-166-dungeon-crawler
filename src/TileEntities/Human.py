from TileEntities.Agent import Agent
from TileEntities.AbstractInteractionMethods import AbstractInteractionMethods
from TileEntities.Monster import Monster

class Human(Agent):
	team = 'human'
	maxHitPoints = 100
	attackDamage = 10
	# action cost is how many turns it will take to do an action
	perceptionViewDistance = 6
	actionCost = 2
	weaponName = "sword"
	weaponDamage = 5
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
		#self.moveDirection('right')
		self.log("Human end log")

