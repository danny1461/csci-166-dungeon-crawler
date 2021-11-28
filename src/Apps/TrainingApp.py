from typing import Any
from Aliases import Features
from Apps.Abstract import Abstract as AbstractApp
from TileEntities.AbstractHitpointEntity import AbstractHitpointEntity
from TileEntities.AbstractTrainableEntity import AbstractTrainableEntity
from GridWorld import GridWorld
from TileEntities.Agent import Agent
from TileEntities.Abstract import Abstract as AbstractTileEntity
from Utils.Cli import commandLineArgs
import os
from random import choice, random

class TrainingApp(AbstractApp):
	def __init__(self):
		self.entities = {}

	def start(self):
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

		for entity in self.entities:
			print('after', entity.weights)

	def setGridWorld(self, world: GridWorld):
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
				self.startTrackingEntity(entity)

		while len(self.gridWorld.teams['agent']) > 0:
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
						if random() < commandLineArgs.episolon:
							action = choice(entity.getAllActions())
							entity.takeAction(action)
						else:
							entity.tick()
					else:
						entity.tick()

					if isinstance(entity, Agent) and entity.pos == self.gridWorld.exitPos:
						toRemove.append((team, entity))
			# round complete, train entities
			for entity in self.entities:
				reward = self.evaluateReward(entity)
				entity.learnFromExperience(self.getPriorFeatures(entity), reward)

			for team, entity in toRemove:
				self.gridWorld.teams[team].remove(entity)
				self.gridWorld.map[entity.pos].remove(entity)
				self.gridWorld.entities.pop(entity)

		self.iterLeft -= 1

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