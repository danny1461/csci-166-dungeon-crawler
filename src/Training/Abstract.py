from typing import Any
from GridWorld import GridWorld
from TileEntities.AbstractTrainableEntity import AbstractTrainableEntity
from abc import ABC, abstractmethod
from Aliases import EventLog, Features

class Abstract(ABC):
	def __init__(self, gridWorld: GridWorld):
		self.gridWorld = gridWorld
		self.training = False

	@property
	def isTraining(self):
		return self.training

	@abstractmethod
	def getFeatures(self, entity: AbstractTrainableEntity) -> Features:
		pass

	@abstractmethod
	def evaluateReward(self, entity: AbstractTrainableEntity, eventLog: EventLog) -> float:
		pass