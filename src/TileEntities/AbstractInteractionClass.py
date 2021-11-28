from TileEntities.Abstract import Abstract
from Aliases.Tile import Tile
from TileEntities.Agent import Agent

class AbstractInteractionEntity(Abstract):
	# we will collect all the defined agents in here 
	# (collected by constructor on creation of agent types, they are manually defined for now)
	overallEntities = {}
	interactionPossible = []
	fightPossible = []
	sightPossible = []

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.overallEntities = self.allEntities
		self.interactable = self.interactionPossible

	# to see the interactable entities and add them to possible interactions
	def setPossibleInteractions(self, this: Agent):
		print(self.interactionPossible)
		#print(Agent(self.interactionPossible[0]))

	## find a match case of an entity
	#def match(self, check: Agent):
	#	for x in self.entities:
	#		if (x == check):
	#			return True

	## basic entity fighting with interactable entities
	#def fight(self: Agent, target: Agent):
	#	self.canWeaponReachTarget(target.pos)
	#	if (self.weaponDoesHit):
	#		self.attackTile(target.pos)
