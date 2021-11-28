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
	direction = "left"

	def tick(self):
		self.log(self.pos)
		#self.log(self.turn)
		#self.actionCounter(self.actionCost)
		#self.log(self.randomPercent)
		#self.actionChance(1)
		#self.log(self.chanceSuccessful)
		#self.eyes((2,2), 10)
		#print("Did see the object: ", self.didSee)
		#self.hasLineOfSight((2,2))
		#print("Line of sight: ", self.los)
		#self.move((2,10))
		if(self.pos[0] == 1):
			self.direction = "right"
		self.moveDirection(self.direction)
		self.log("Agent end log")