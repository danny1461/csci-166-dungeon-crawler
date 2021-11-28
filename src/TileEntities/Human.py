from TileEntities.Agent import Agent
from TileEntities.AbstractInteractionClass import AbstractInteractionEntity
from TileEntities.Monster import Monster

class Human(Agent, AbstractInteractionEntity):
	team = 'human'
	maxHitPoints = 100
	attackDamage = 10
	# action cost is how many turns it will take to do an action
	viewDistance = 5
	actionCost = 2
	weaponName = "sword"
	weaponDamage = 5
	weaponDamageMultiplier = 2.0
	weaponReach = 1

	attackDamage = weaponDamage

	def __init__(self, *args, **kwargs):
		self.interactionPossible.append(self)
		super().__init__(*args, **kwargs)
		self.attackDamage = self.weaponDamage

	def tick(self):
		print()
		self.setPossibleInteractions(self)
		print(self.attackDamage)

