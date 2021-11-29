from TileEntities.Abstract import Abstract
from TileEntities.Agent import Agent
#from Aliases.Tile import Tile

class AbstractInteractionMethods(Abstract):
	# we will collect all the defined agents in here 
	# (collected by constructor in creation of agent types, they are manually defined for now)
	overallEntities = {}
	interactionPossible = [Agent]
	fightPossible = [Agent]
	sightPossible = [Agent]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.overallEntities = self.allEntities
		self.interactable = self.interactionPossible

	# to remove duplicates from a desired list
	def __removeListDuplicates(desList: list):
		return list(dict.fromkeys(desList))

	# show the possible interactions an agent can take
	def showPossibleInteractions(thisAgent: Agent):
		thisAgent.log("Agent", thisAgent.team, ":")
		thisAgent.log("Has seen:", AbstractInteractionMethods.sightPossible)
		thisAgent.log("Can fight:", AbstractInteractionMethods.fightPossible)

	# find a match case of an entity in the world
	def match(check: Agent):
		for x in AbstractInteractionMethods.overallEntities:
			if (x == check):
				return x

	# to see the interactable entities and add them to possible interactions
	def checkPossibleInteractions(thisAgent: Agent):
		AbstractInteractionMethods.sightPossible = []
		AbstractInteractionMethods.fightPossible = []
		for i in AbstractInteractionMethods.interactionPossible:
			if (i.team != 'agent'):
				thisAgent.eyes(i.pos)

				#print(thisAgent.team, thisAgent.pos, thisAgent.perceptionViewDistance)
				#print(i.team, i.pos, i.perceptionViewDistance)
				#print(thisAgent.didSee)
				
				if (thisAgent.didSee):
					AbstractInteractionMethods.sightPossible.append(i)
				thisAgent.setIfWeaponReachTarget(i.pos)
				
				if (thisAgent.weaponDoesHit):
					AbstractInteractionMethods.fightPossible.append(i)
				
				AbstractInteractionMethods.fightPossible = AbstractInteractionMethods.__removeListDuplicates(AbstractInteractionMethods.fightPossible)
				AbstractInteractionMethods.sightPossible = AbstractInteractionMethods.__removeListDuplicates(AbstractInteractionMethods.sightPossible)

		
		#AbstractInteractionMethods.showPossibleInteractions(thisAgent)

	# find a match case of an entity in the world
	# not sure if it works, check later
	def match(check: Agent):
		for x in AbstractInteractionMethods.overallEntities:
			if (x == check):
				return x

	# basic entity fighting with interactable entities
	# example, but it is a bit broken (nonetype errors pop up once agents are dead)
	def fight(attacker: Agent):
		#print("Fighters:",AbstractInteractionMethods.fightPossible)
		fighting = [x for x in AbstractInteractionMethods.fightPossible if x.team != attacker.team]
		#print("->>>>>>>>>>>>>>>",fighting)
		if (len(fighting)):
			#print(fighting[0], "has been hit")
			attacker.attackTile(fighting[0].pos)
