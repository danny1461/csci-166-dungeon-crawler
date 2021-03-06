from Aliases import Features
from Apps.Abstract import Abstract as AbstractApp
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractTrainableEntity import AbstractTrainableEntity
from TileEntities.Agent import Agent
from TileEntities.Abstract import Abstract as AbstractTileEntity
from Utils.Cli import commandLineArgs
import os
from random import choice, random
import json

class TrainingApp(AbstractApp):
	def __init__(self):
		self.entities = {}

	def start(self):
		from GridWorld import GridWorld

		mapPath = os.path.join(os.getcwd(), '../dungeons/', commandLineArgs.map + '.txt')
		f = open(mapPath, 'r')
		try:
			self.mapData = f.read()
		finally:
			f.close()

		self.setGridWorld(GridWorld(fromString = self.mapData))
		self.iterLeft = commandLineArgs.trainIter
		while self.iterLeft > 0:
			print('Iterations Left: ', self.iterLeft)
			self.setGridWorld(GridWorld(fromString = self.mapData))
			self.runIter()

		self.saveWeights()

	def saveWeights(self):
		for entity in self.entities:
			aiPath = os.path.join(os.getcwd(), '../ai/', self.trainer.__class__.__name__ + '_' + entity.__class__.__name__ + '.json')
			f = open(aiPath, 'w')
			try:
				f.write(json.dumps(entity.weights))
			finally:
				f.close()

	def setGridWorld(self, world):
		AbstractTileEntity.resetNextEntityId()
		self.gridWorld = world

		trainClass = commandLineArgs.trainClass
		self.trainer = trainClass(self.gridWorld)

		if len(self.entities):
			for entity in self.entities:
				newEntity = self.gridWorld.getEntityById(entity.id)
				newEntity.weights = entity.weights

	def runIter(self):
		self.entities = {}
		for entity in self.gridWorld.entities:
			if isinstance(entity, AbstractTrainableEntity):
				entity.setTrainer(self)
				entity.onAction.on(self.onEvent)

		ticks = 0
		while len(self.gridWorld.teams['agent']) > 0 and ticks < 1000:
			for entity in self.gridWorld.entities:
				if isinstance(entity, AbstractTrainableEntity):
					self.startTrackingEntity(entity)

			toRemove = []
			for team in self.gridWorld.teamList:
				self.gridWorld.currentTeam = team

				for entity in self.gridWorld.teams[self.gridWorld.currentTeam]:
					if isinstance(entity, AbstractHitpointEntity) and entity.isDead:
						self.gridWorld.log('Entity {} at {},{} died'.format(entity.__class__.__name__, entity.x, entity.y))
						toRemove.append((team, entity))
						continue

					if isinstance(entity, AbstractTrainableEntity):
						# random action or intentional?
						if random() < commandLineArgs.epsilon:
							action = choice(list(entity.getAllActions()))
							entity.takeAction(action)
						else:
							entity.tick()
					else:
						entity.tick()

					if isinstance(entity, Agent) and entity.pos == self.gridWorld.exitPos:
						toRemove.append((team, entity))

			# round complete, train entities
			ticks += 1

			for entity in self.entities:
				reward = self.evaluateReward(entity)
				entity.learnFromExperience(self.getPriorFeatures(entity), reward)

			for team, entity in toRemove:
				self.gridWorld.teams[team].remove(entity)
				self.gridWorld.map[entity.pos].remove(entity)
				self.gridWorld.entities.pop(entity)

		self.iterLeft -= 1
		for entity in self.entities:
			print(entity.__class__.__name__, entity.weights)

	def onEvent(self, entity, eventName, params):
		if self.gridWorld.isTrackingActions:
			return

		if entity not in self.entities:
			return

		params['event'] = eventName
		self.entities[entity]['events'].append(params)

	def getPriorFeatures(self, entity):
		if entity not in self.entities:
			return None

		return self.entities[entity]['features']

	def getEvents(self, entity):
		if entity not in self.entities:
			return []

		return self.entities[entity]['events']

	def startTrackingEntity(self, entity):
		self.entities[entity] = {
			'features': self.trainer.getFeatures(entity),
			'events': []
		}

	def startSimulating(self):
		self.gridWorld.trackActions()

	def stopSimulating(self):
		self.gridWorld.rollbackActions()

	def getFeatures(self, entity: AbstractTrainableEntity) -> Features:
		return self.trainer.getFeatures(entity)

	def evaluateReward(self, entity: AbstractTrainableEntity) -> float:
		return self.trainer.evaluateReward(entity, self.getEvents(entity))