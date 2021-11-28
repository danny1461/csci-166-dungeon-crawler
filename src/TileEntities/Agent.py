from TileEntities.AbstractMovableEntity import AbstractMovableEntity
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractAggresiveEntity import AbstractAggresiveEntity
from TileEntities.AbstractActionEntity import AbstractActionEntity
from TileEntities.AbstractPerceptionEntity import AbstractPerceptionEntity

class Agent(AbstractMovableEntity, AbstractHitpointEntity, AbstractAggresiveEntity, AbstractActionEntity, AbstractPerceptionEntity):
	team = 'agent'
	maxHitPoints = 100
	attackDamage = 10
	# action cost is how many turns it will take to do an action
	actionCost = 3

	def tick(self):

		#self.log(self.pos)
		#self.log(self.turn)
		#self.actionCounter(self.actionCost)
		#self.log(self.randomPercent)
		#self.actionChance(1)
		#self.log(self.chanceSuccessful)
		#self.eyes((2,2), 50)
		#print(self.didSee)
		#self.isLineOfSightBlocked((2,2))
		#self.move((2,10))
		#self.moveDirection("left")
		#print(self.losBlocked)
		self.log("Agent end log")